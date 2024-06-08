from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .models import User, Wallet, Transaction

def welcome_page(request):
    return render(request, 'welcome.html')

def login_page(request):
    return render(request, 'login.html')

def sign_up_page(request):
    return render(request, 'signup.html')

def forgot_password_page(request):
    return render(request, 'forgot_password.html')

def contact_page(request):
    return render(request, 'contact.html')

def profile_page(request):
    return render(request, 'profile.html')

def wallet_page(request):
    return render(request, 'wallet.html')
