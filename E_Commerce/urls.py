from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, ),
    path('accounts', views.account),
    path('signup', views.signup),
    path('cart', views.cart),
    path('welcome', views.welcome),
    path('storesetup', views.store_setup),
    path('paymentsetup', views.payment_setup),
    path('ready', views.ready),
    path('activate/<uidb64>/<token>/',views.activate, name='activate'),
    path('login', views.login),
    path('activation_email/<username>/', views.activation_email),
    path('accounts/lost-password', views.lost_password),
    path('accounts/emailpassword', views.lost_password_email),
    path('accounts/reset-password/<username>/', views.reset_password),
    path('accounts/profile', views.profile),
    path('accounts/orders', views.orders),
    path('accounts/downloads', views.downloads),
    path('accounts/addresses', views.addresses),
    path('password_reset/<uidb64>/<token>/',views.password_reset, name='password_reset'),
    path('accounts/reset-password/<username>/new-password', views.new_password),

]
