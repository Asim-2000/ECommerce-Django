from django.shortcuts import render, redirect
from E_Commerce.models import *
from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError


# Create your views here.

def home(request):
    return render(request, 'E_Commerce/HomePage.html')


def account(request):
    return render(request, 'E_Commerce/Login_Registration.html')


def signup(request):
    if request.method == "POST":
        email = request.POST["email"]
        firstname = request.POST["firstname"]
        lastname = request.POST["last_name"]
        password = request.POST["Password"]
        contact_number = request.POST["contact_number"]
        try:
            user_role = request.POST['customer_vendor']
            if user_role == "customer":
                user = CUSTOMER()
                user.email = email
                user.firstname = firstname
                user.lastname = lastname
                user.password = password
                user.contact_number = contact_number
                user.username = user.generate_username(email)
                user.save()
                return redirect("/")
            elif user_role == "vendor":
                user = VENDOR()
                user.email = email
                user.firstname = firstname
                user.lastname = lastname
                user.password = password
                user.contact_number = contact_number
                user.save()
                return redirect("/")
        except(MultiValueDictKeyError):
            return HttpResponse("404 Error")
    else:
        return HttpResponse("404 not Found")
