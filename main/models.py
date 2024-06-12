from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=9, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    def __str__(self):
        return self.user.username

class Transaction(models.Model):
    from_account = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='from_account')
    to_account = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='to_account', null=True, blank=True)
    transaction_type = models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
