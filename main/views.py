from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm, UserLoginForm, TransactionForm
from .models import Profile, Transaction
import random

def generate_account_number():
    return ''.join(random.choices('0123456789', k=12))

def welcome(request):
    return render(request, 'main/index.html')

def login_signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            if Profile.objects.filter(user=user).exists():
                return render(request, 'main/login_signup.html', {'form': form, 'error': 'You already have an account'})
            user.save()
            Profile.objects.create(user=user, account_number=generate_account_number())
            login(request, user)
            return redirect('profile')
    else:
        form = UserRegistrationForm()
    return render(request, 'main/login_signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')
    else:
        form = UserLoginForm()
    return render(request, 'main/login_signup.html', {'form': form})

def profile(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            to_account_number = form.cleaned_data['to_account']
            if to_account_number:
                try:
                    to_profile = Profile.objects.get(account_number=to_account_number)
                    if profile.balance < amount:
                        return render(request, 'main/profile.html', {'profile': profile, 'form': form, 'error': 'Insufficient savings'})
                    Transaction.objects.create(
                        from_account=profile,
                        to_account=to_profile,
                        transaction_type='transfer',
                        amount=amount
                    )
                    profile.balance -= amount
                    profile.save()
                    to_profile.balance += amount
                    to_profile.save()
                    return redirect('wallet')
                except Profile.DoesNotExist:
                    return render(request, 'main/profile.html', {'profile': profile, 'form': form, 'error': 'Invalid account number'})
            else:
                Transaction.objects.create(
                    from_account=profile,
                    transaction_type='deposit',
                    amount=amount
                )
                profile.balance += amount
                profile.save()
                return redirect('wallet')
    else:
        form = TransactionForm()
    return render(request, 'main/profile.html', {'profile': profile, 'form': form})

def wallet(request):
    profile = Profile.objects.get(user=request.user)
    transactions = Transaction.objects.filter(from_account=profile) | Transaction.objects.filter(to_account=profile)
    transactions = transactions.order_by('-timestamp')
    return render(request, 'main/wallet.html', {'profile': profile, 'transactions': transactions})

def forgot_password(request):
    if request.method == 'POST':
        # Add logic for password reset here
        pass
    return render(request, 'main/forgot_password.html')
