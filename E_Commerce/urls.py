from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, ),
    path('accounts', views.account),
    path('signup', views.signup),
    path('cart', views.cart),
    path('welcome', views.welcome),

]