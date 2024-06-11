from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
import random
from django.contrib import messages
from .supabase_client import supabase

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
            return redirect('register')

        user = User.objects.create_user(username=name, email=email, password=password)
        user.save()

        # Add user to Supabase
        response = supabase.from_('users').insert({
            'username': name,
            'email': email,
            'password': password,
        }).execute()
        
        if response.error:
            messages.error(request, 'Error in Supabase')
            return redirect('register')

        messages.success(request, 'Account created successfully')
        return redirect('login')
    return render(request, 'login')

def login_signup(request):
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
    return render(request, 'login')

