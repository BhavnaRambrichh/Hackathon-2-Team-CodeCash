from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
import random
from django.contrib import messages
from .supabase_client import supabase
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Transaction, Profile


def generate_account_number():
    return ''.join(random.choices('0123456789', k=12))

def welcome(request):
    return render(request, 'main/index.html')

def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']

        # Check if user already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('login')
        
        account_number = generate_account_number()
        user = User.objects.create_user(username=name, email=email, password=password)
        user.profile.account_number = account_number
        user.save()

        # Add user to Supabase
        response = supabase.from_('users').insert({
            'username': name,
            'email': email,
            'password': password,
        }).execute()
        
        if response.error:
            messages.error(request, 'Error in Supabase')
            return redirect('login')

        messages.success(request, 'Account created successfully')
        return redirect('login_signup')
    return render(request, 'main/login.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    return render(request, 'main/login.html')


@login_required
def profile_view(request):
    user = request.user
    profile = Profile.objects(User)
    context = {
        'full_name': user.get_full_name(),
        'email': user.email,
        'account_number': profile.account_number,
    }
    return render(request, 'main,/profile.html', context)


@login_required
def add_money(request):
    if request.method == 'POST':
        amount = float(request.POST['amount'])
        user = request.user
        account_number = user.profile.account_number

        # Add money 
        response = supabase.from_('transactions').insert({
            'datetime': timezone.now(),
            'from_account': account_number,
            'to_account': account_number,
            'amount': amount,
            'transaction_type': 'deposit'
        }).execute()

        if response.error:
            messages.error(request, 'Error in Supabase')
        else:
            messages.success(request, 'Money added successfully')

        return redirect('profile')

    return render(request, 'main/add_money.html')

@login_required
def withdraw_money(request):
    if request.method == 'POST':
        amount = float(request.POST['amount'])
        user = request.user
        account_number = user.profile.account_number

        # Check if user has enough balance
        response = supabase.from_('transactions').select('amount').eq('to_account', account_number).execute()
        if response.error:
            messages.error(request, 'Error in Supabase')
            return redirect('profile')
        
        balance = sum([t['amount'] for t in response.data])
        
        if amount > balance:
            messages.error(request, 'Insufficient savings')
        else:
            # Withdraw money 
            response = supabase.from_('transactions').insert({
                'datetime': timezone.now(),
                'from_account': account_number,
                'to_account': account_number,
                'amount': -amount,
                'transaction_type': 'withdrawal'
            }).execute()

            if response.error:
                messages.error(request, 'Error in Supabase')
            else:
                messages.success(request, 'Money withdrawn successfully')

        return redirect('profile')

    return render(request, 'main/withdraw_money.html')

@login_required
def transfer_money(request):
    if request.method == 'POST':
        amount = float(request.POST['amount'])
        to_account = request.POST['to_account']
        user = request.user
        from_account = user.profile.account_number

        # Check if user has enough balance
        response = supabase.from_('transactions').select('amount').eq('to_account', from_account).execute()
        if response.error:
            messages.error(request, 'Error in Supabase')
            return redirect('profile')
        
        balance = sum([t['amount'] for t in response.data])

        if amount > balance:
            messages.error(request, 'Insufficient savings')
        else:
            # Transfer money 
            response = supabase.from_('transactions').insert({
                'datetime': timezone.now(),
                'from_account': from_account,
                'to_account': to_account,
                'amount': amount,
                'transaction_type': 'transfer'
            }).execute()

            if response.error:
                messages.error(request, 'Error in Supabase')
            else:
                messages.success(request, 'Money transferred successfully')

        return redirect('profile')

    return render(request, 'main/transfer_money.html')

@login_required
def wallet_view(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-timestamp')
    
    # Calculate the balance
    balance = 0
    for transaction in transactions:
        if transaction.transaction_type == 'deposit':
            balance += transaction.amount
        elif transaction.transaction_type in ['withdraw', 'transfer']:
            balance -= transaction.amount

    return render(request, 'wallet.html', {'transactions': transactions, 'balance': balance})

