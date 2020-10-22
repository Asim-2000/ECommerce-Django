from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import render, redirect
from .models import Customer, Vendor
from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.core.mail import send_mail


# Create your views here.


def home(request):
    return render(request, 'E_Commerce/HomePage.html')


def account(request):
    return render(request, 'E_Commerce/Login_Registration.html')


def cart(request):
    return render(request, 'E_Commerce/Cart.html')


def welcome(request):
    return render(request, 'E_Commerce/Welcome.html')


def signup(request):
    if request.method == "POST":
        email = request.POST["email"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        password = request.POST["Password"]
        confirm_password = request.POST["ConfirmPassword"]
        contact_number = request.POST["contact_number"]
        try:
            user_role = request.POST['customer_vendor']
            if user_role == "customer":
                if password == confirm_password:
                    user = Customer()
                    user.create_Customer(firstname, lastname, email, password, contact_number)
                    if user.created:
                        send_mail('subject', 'body of the message', 'noreply@karkhanay.com', [email])
                        return redirect("/")
                else:
                    messages.error(request, "Error: Password does not match.")
                    return redirect("/accounts")

            elif user_role == "vendor":
                if password == confirm_password:
                    user = Vendor()
                    user.create_Vendor(email, firstname, lastname, contact_number, password)
                    return redirect("/")
                else:
                    messages.error(request, "Error: Password does not match.")
                    return redirect("/accounts")

        except MultiValueDictKeyError:
            return redirect("/accounts")
        except TypeError:
            messages.error(request, "Invalid First or Last Name")
            return redirect("/accounts")
        except IntegrityError:
            messages.error(request, "You are already signed up.")
            return redirect("/accounts")
        except ValueError:
            messages.error(request, "Invalid Contact Number")
            return redirect("/accounts")
        else:
            messages.error(request, "Please select one of the category.")
            return redirect("/accounts")
    else:
        return HttpResponse("404 not Found")
