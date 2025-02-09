from django.urls import path
from . import views

urlpatterns = [
path("", views.home, name="home"),
path("withdraw/", views.withdraw_view, name="withdraw"),
path("transactions/", views.transactions, name='transactions'),
path("deposit/", views.deposit_view, name='deposit'),
path("transfer/", views.transfer_view, name="transfer"),
path('login/', views.login_view, name='login'),
path("register/", views.register, name="register"),
path('logout/', views.logout_view, name='logout'),
path('transaction_success/', views.transaction_success, name='transaction_success'),
]
