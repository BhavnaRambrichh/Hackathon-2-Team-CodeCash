from django import forms
from django.contrib.auth.models import User

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class SignInForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class TransactionForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    to_account = forms.CharField(max_length=12, required=False)
