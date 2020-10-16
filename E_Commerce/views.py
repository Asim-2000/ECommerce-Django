from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def home(request):
    return render(request, 'E_Commerce/HomePage.html')


def account(request):
    return render(request, 'E_Commerce/Login_Registration.html')
