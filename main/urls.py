from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('login_signup/', views.index, name='login_signup'),
    path('profile/', views.profile_view, name='profile'),
    path('wallet/', views.wallet_view, name='wallet'),
    path('add_money/', views.add_money, name='add_money'),
    path('withdraw_money/', views.withdraw_money, name='withdraw_money'),
    path('transfer_money/', views.transfer_money, name='transfer_money'),
]
