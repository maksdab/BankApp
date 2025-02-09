from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Customer

class SignUpForm(UserCreationForm):
    address = forms.CharField(max_length=100)
    phone_number = forms.CharField(max_length=20)
    date_of_birth = forms.DateField()

    class Meta:
        model = User
        fields = ('username', 'address', 'phone_number', 'date_of_birth', 'password1', 'password2')

class LoginForm(forms.Form):
    username = forms.CharField(label="username")
    password = forms.CharField(label="password", widget=forms.PasswordInput)

class TransferForm(forms.Form):
    receiver_account_number = forms.CharField(label='Receiver Account Number', max_length=20)
    amount = forms.DecimalField(label='Amount', max_digits=10, decimal_places=2)

class DepositForm(forms.Form):
    amount = forms.DecimalField(label='Amount', max_digits=10, decimal_places=2)

class WithdrawForm(forms.Form):
    amount = forms.DecimalField(label='Amount', max_digits=10, decimal_places=2)