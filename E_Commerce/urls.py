from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, ),
    path('accounts', views.account),
    path('signup', views.signup),
    path('cart', views.cart),
    path('welcome', views.welcome),
    path('storesetup', views.storeSetup),
    path('paymentsetup', views.paymentSetup),
    path('ready', views.ready),
    path('activate/<uidb64>/<token>/',views.activate, name='activate'),
    path('login', views.login),
    path('activation_email/<username>/', views.activation_email),
    path('accounts/lost-password', views.lost_password),
]