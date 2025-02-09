from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    date_of_birth = models.DateField()

    def __str__(self):
        return self.user.username

class AccountData(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=20, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.account_number


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('TRANSFER', 'Transfer'),
        ('DEPOSIT', 'Deposit'),
        ('WITHDRAW', 'Withdraw'),
    )

    account = models.ForeignKey(AccountData, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    related_account = models.CharField(max_length=20, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"



class Transfer(models.Model):
    sender_account = models.ForeignKey(AccountData, on_delete=models.CASCADE, related_name='sender_transfers')
    receiver_account = models.ForeignKey(AccountData, on_delete=models.CASCADE, related_name='receiver_transfers')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transfer from {self.sender_account} to {self.receiver_account} - {self.amount}"


class Deposit(models.Model):
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, primary_key=True)


class Withdraw(models.Model):
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, primary_key=True)
    
