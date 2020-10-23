from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .models import Customer, Vendor
from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password

# Create your views here.
from .tokens import account_activation_token


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
                    user.create_Customer(firstname, lastname, email, make_password(password), contact_number)
                    user.sendEmail(user,request)
                    messages.info(request, "Account Created Successfully. Verify your email.")
                    return redirect("/accounts")
                else:
                    messages.error(request, "Error: Password does not match.")
                    return redirect("/accounts")

            elif user_role == "vendor":
                if password == confirm_password:
                    user = Vendor()
                    user.create_Vendor(email, firstname, lastname, contact_number, make_password(password))
                    user.sendEmail(user,request)
                    messages.info(request, "Account Created Successfully. Verify your email.")
                    return redirect("/accounts")
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


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Customer.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Customer.DoesNotExist):
        user = Vendor.objects.get(pk=uid)
    if user is not None and account_activation_token.check_token(user, token):
        user.verified = True
        user.save()
        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect("/accounts")
    else:
        return HttpResponse('Activation link is invalid!')


def login(request):
    if request.method == "POST":
        u_name = request.POST["u_name"]
        password_login = request.POST["password_login"]
        user = Customer()
        try:
            if user.login(u_name, password_login):
                return HttpResponse("SUCCESS")
            else:
                messages.error(request, "Invalid Username/Password")
                return redirect("/accounts")
        except AssertionError:
            messages.error(request, "Verify your email.")
            return redirect("/accounts")
        except Customer.DoesNotExist:
            messages.error(request, "Invalid Username/Password")
            return redirect("/accounts")