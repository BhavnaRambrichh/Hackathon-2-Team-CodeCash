from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('login_signup/', views.login_signup, name='login_signup'),
    path('profile/', views.profile, name='profile'),
    path('wallet/', views.wallet, name='wallet'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('add_money/', views.add_money, name='add_money'),
]
