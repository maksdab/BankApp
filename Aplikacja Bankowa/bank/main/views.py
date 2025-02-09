from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import SignUpForm, LoginForm, TransferForm, DepositForm, WithdrawForm
from django.contrib import messages
from django.contrib.auth.models import User  
from .models import Customer, AccountData, Transaction, Deposit, Withdraw
import random

def home(request):
    return render(request, 'main/home.html')

def transactions(request):
    if hasattr(request.user, 'customer'):
        customer = request.user.customer
        account = customer.accountdata_set.first()
        if account:
            transactions = account.transactions.all()  # Pobieramy wszystkie transakcje powiązane z kontem
        else:
            transactions = []
    else:
        transactions = []
        
    return render(request, 'main/transactions.html', {'transactions': transactions})

def transfer_view(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            receiver_account_number = form.cleaned_data['receiver_account_number']
            
            if hasattr(request.user, 'customer'):
                customer = request.user.customer
                # Ensure we use the correct way to get the account
                sender_account = customer.accountdata_set.first()
                
                if sender_account:
                    print("Sender account:", sender_account)  # Sprawdźmy, czy sender_account jest prawidłowo przypisany
                    
                    try:
                        receiver_account = AccountData.objects.get(account_number=receiver_account_number)
                        print("Receiver account:", receiver_account)
                    except AccountData.DoesNotExist:
                        messages.error(request, 'Receiver account does not exist.')
                        return redirect('transfer')
                    
                    if sender_account.balance >= amount:
                        # Utwórz transakcję w bazie danych
                        transaction = Transaction.objects.create(
                            account=sender_account,
                            amount=-amount,
                            transaction_type='TRANSFER',
                            related_account=receiver_account.account_number
                        )
                        # Zaktualizuj saldo konta źródłowego
                        sender_account.balance -= amount
                        sender_account.save()
                        # Zaktualizuj saldo konta docelowego
                        receiver_account.balance += amount
                        receiver_account.save()
                        # Przekieruj użytkownika do strony powiadomienia o udanej transakcji
                        return redirect('transaction_success')
                    else:
                        # Przekieruj użytkownika do strony błędu (brak wystarczających środków)
                        messages.error(request, 'Insufficient funds.')
                        return redirect('transfer')
                else:
                    messages.error(request, 'No bank account assigned to this user.')
                    return redirect('transfer')
            else:
                messages.error(request, 'No customer assigned to this user.')
                return redirect('transfer')
    else:
        form = TransferForm()
    return render(request, 'main/transfer.html', {'form': form})

def withdraw_view(request):
    if request.method == 'POST':
        form = WithdrawForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            customer = request.user.customer
            account = customer.accountdata_set.first()

            if account.balance >= amount:
                # Utwórz transakcję wypłaty w bazie danych
                transaction = Transaction.objects.create(
                    account=account,
                    amount=-amount,
                    transaction_type='WITHDRAW'
                )
                # Zaktualizuj saldo konta
                account.balance -= amount
                account.save()

                
                # Przekieruj użytkownika do strony powiadomienia o udanej wypłacie
                return redirect('transaction_success')
            else:
                messages.error(request, 'Insufficient funds.')
                # Przekieruj użytkownika do strony błędu (brak wystarczających środków)
                return redirect('withdraw')
    else:
        form = WithdrawForm()
    return render(request, 'main/withdraw.html', {'form': form})

def deposit_view(request):
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            customer = request.user.customer
            account = customer.accountdata_set.first()  # Uzyskaj pierwsze konto użytkownika
            # Utwórz transakcję depozytu w bazie danych
            transaction = Transaction.objects.create(
                account=account,
                amount=amount,
                transaction_type='DEPOSIT'
            )
            # Zaktualizuj saldo konta
            account.balance += amount
            account.save()
            # Przekieruj użytkownika do strony powiadomienia o udanym depozycie
            return redirect('transaction_success')
    else:
        form = DepositForm()
    return render(request, 'main/deposit.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Przekieruj użytkownika po zalogowaniu
                return redirect('home')
            else:
                # Obsłuż błąd uwierzytelniania
                error_message = "Invalid username or password."
    else:
        form = LoginForm()
        error_message = None
    return render(request, 'main/login.html', {'form': form, 'error_message': error_message})

def logout_view(request):
    logout(request)
    messages.success(request, "Zostałeś poprawnie wylogowany.")
    print(messages.get_messages(request))
    return redirect('home') # Po wylogowaniu przekierowujemy użytkownika na stronę główną

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            address = form.cleaned_data['address']
            phone_number = form.cleaned_data['phone_number']
            date_of_birth = form.cleaned_data['date_of_birth']
            
            user = User.objects.create_user(username=username, password=form.cleaned_data['password1'])
            if user is None:
                messages.error(request, 'Failed to create user account.')
                return redirect('register')
            
            print("User created successfully")
            print(f"Username: {user.username}")
            
            customer = Customer.objects.create(user=user, address=address, phone_number=phone_number, date_of_birth=date_of_birth)
            if customer is None:
                user.delete()
                messages.error(request, 'Failed to create customer profile.')
                return redirect('register')
            
            print("Customer profile created successfully")
            print(f"Address: {customer.address}")
            
            account_number = generate_account_number()
            balance = 0
            account_data = AccountData.objects.create(customer=customer, account_number=account_number, balance=balance)
            if account_data is None:
                user.delete()
                customer.delete()
                messages.error(request, 'Failed to create bank account.')
                return redirect('register')
            
            print("Bank account created successfully")
            print(f"Account number: {account_data.account_number}")
            
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'main/register.html', {'form': form})



def generate_account_number():
    return ''.join(random.choices('0123456789', k=20))

def transaction_success(request):
    last_transaction = Transaction.objects.latest('date')
    transaction_number = last_transaction.pk  # Numer transakcji to identyfikator główny (primary key)
    return render(request, 'main/transaction_success.html', {'transaction_number': transaction_number})