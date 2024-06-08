from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10)
    datetime_of_transfer = models.DateTimeField(auto_now_add=True)
    from_account = models.CharField(max_length=20)
    to_account = models.CharField(max_length=20)
    monetary_value = models.DecimalField(max_digits=10, decimal_places=2)