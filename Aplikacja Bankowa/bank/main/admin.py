from django.contrib import admin

from .models import Customer, AccountData, Transaction, Transfer, Deposit, Withdraw

admin.site.register(Transaction)
admin.site.register(Transfer)
admin.site.register(Deposit)
admin.site.register(Withdraw)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'address', 'phone_number', 'date_of_birth']  # Pola, które chcesz wyświetlić w tabeli

admin.site.register(Customer, CustomerAdmin)

class AccountDataAdmin(admin.ModelAdmin):
    list_display = ['customer', 'account_number', 'balance']  # Pola, które chcesz wyświetlić w tabeli

admin.site.register(AccountData, AccountDataAdmin)
