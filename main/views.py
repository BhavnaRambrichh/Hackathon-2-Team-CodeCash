from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import random
from django.contrib import messages
from .supabase_client import supabase
from django.utils import timezone
from .models import Transaction, Profile
from .forms import SignUpForm, SignInForm

def generate_account_number():
    return ''.join(random.choices('0123456789', k=12))

def welcome(request):
    return render(request, 'main/index.html')

# views.py

def index(request):
    if request.method == 'POST':
        if 'sign_up' in request.POST:
            signup_form = SignUpForm(request.POST)
            signin_form = SignInForm()
            
            if signup_form.is_valid():
                user = signup_form.save()
                login(request, user)
                return redirect('login_signup')  # Redirect to home page after successful sign up
        
        elif 'sign_in' in request.POST:
            signin_form = SignInForm(data=request.POST)
            signup_form = SignUpForm()
            if signin_form.is_valid():
                user = authenticate(username=signin_form.cleaned_data.get('username'), password=signin_form.cleaned_data.get('password'))
                if user is not None:
                    login(request, user)
                    return redirect('profile')  # Redirect to home page after successful login
    else:
        signup_form = SignUpForm()
        signin_form = SignInForm()
    return render(request, 'main/template/main/login_signup.html', {'signup_form': signup_form, 'signin_form': signin_form})


































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
    return render(request, 'main/login_html.html')


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

