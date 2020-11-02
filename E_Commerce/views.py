from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from .models import Customer, Vendor
from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.hashers import make_password

# Create your views here.
from .models.User import User
from .tokens import account_activation_token, password_reset_token


def home(request):
    return render(request, 'E_Commerce/HomePage.html')


def account(request):
    return render(request, 'E_Commerce/Login_Registration.html')


def cart(request):
    return render(request, 'E_Commerce/Cart.html')


def store_setup(request):
    return render(request, 'E_Commerce/StoreSetup.html')


def payment_setup(request):
    return render(request, 'E_Commerce/PaymentSetup.html')


def ready(request):
    return render(request, 'E_Commerce/Ready.html')


def orders(request):
    return render(request, 'E_Commerce/Orders.html')


def downloads(request):
    return render(request, 'E_Commerce/Downloads.html')


def addresses(request):
    return render(request, 'E_Commerce/Addresses.html')


def account_details(request):
    return render(request, 'E_Commerce/AccountDetails.html')


def rma_requests(request):
    return render(request, 'E_Commerce/RMA_Requests.html')


def vendors(request):
    return render(request, 'E_Commerce/Vendors.html')


def tickets(request):
    return render(request, 'E_Commerce/Tickets.html')


def signup(request):
    if request.method == "POST":
        email = request.POST["email"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        password = request.POST["Password"]
        confirm_password = request.POST["ConfirmPassword"]
        contact_number = request.POST["contact_number"]
        try:
            if password == confirm_password:
                user = Customer()
                user.create_Customer(firstname, lastname, email, make_password(password), contact_number)
                user.sendEmail(user, request)
                messages.info(request, "Account Created Successfully. Verify your email.")
                return redirect("/customer")
            else:
                messages.error(request, "Error: Password does not match.")
                return redirect("/customer")
        except MultiValueDictKeyError:
            return redirect("/customer")
        except TypeError:
            messages.error(request, "Invalid First or Last Name")
            return redirect("/customer")
        except IntegrityError:
            messages.error(request, "You are already signed up.")
            return redirect("/customer")
        except ValueError:
            messages.error(request, "Invalid Contact Number")
            return redirect("/customer")
    else:
        return HttpResponse("404 not Found")


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Customer.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Customer.DoesNotExist):
        return HttpResponse("404 Error")
    if user is not None and account_activation_token.check_token(user, token):
        user.verified = True
        user.save()
        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect("/customer")
    else:
        return HttpResponse('Activation link is invalid!')


def login(request):
    if request.method == "POST":
        u_name = request.POST["u_name"]
        password_login = request.POST["password_login"]
        user = Customer()
        try:
            if user.login(u_name, password_login):
                request.session['authenticated'] = True
                return render(request, 'E_Commerce/Profile.html')
            else:
                messages.error(request, "Invalid Username/Password")
                return redirect("/customer")
        except AssertionError:
            if "@" in u_name:
                i = u_name.index("@")
                username = u_name[:i]
            else:
                username = u_name
            messages.info(request,
                          "Verify your email. <a href='activation_email/" + username + "/'>Resend</a> verification email")
            return redirect("/customer")
        except User.DoesNotExist:
            messages.error(request, "Invalid Username/Password")
            return redirect("/customer")


def activation_email(request, username):
    user = Customer.objects.get(username=username)
    user.sendEmail(user, request)
    messages.info(request, "Email sent! If you can't find the email, check your spam")
    return redirect("/customer")


def lost_password(request):
    return render(request, 'E_Commerce/LostPassword.html')


def reset_password(request, enc_id):
    return render(request, 'E_Commerce/ResetPassword.html')


def lost_password_email(request):
    if request.method == "POST":
        name_email = request.POST["u_name_email"]
        if "@" in name_email:
            i = name_email.index("@")
            username = name_email[:i]
        else:
            username = name_email
        try:
            user = Customer.objects.get(username=username)
            user.sendPasswordResetEmail(request, user)
            messages.info(request, "Password Reset Email Sent.")
            return redirect("/customer/lost-password")
        except Customer.DoesNotExist:
            messages.error(request, "No such customer exist.")
            return redirect("/customer/lost-password")


def password_reset(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Customer.objects.get(pk=uid)
        enc_id = user.encrypted_id
        if user is not None and password_reset_token.check_token(user, token):
            return redirect("/customer/reset-password/" + enc_id + "/")
        else:
            return HttpResponse('Reset password link is invalid!')
    except(TypeError, ValueError, OverflowError, Customer.DoesNotExist):
        return HttpResponse('Reset password link is invalid!')


def new_password(request, enc_id):
    user = Customer.objects.get(encrypted_id=enc_id)
    if request.method == "POST":
        password = request.POST["newPass"]
        c_password = request.POST["newPassConfirm"]
        if password == c_password:
            user.password = make_password(password)
            user.save()
            messages.success(request, "Password changed successfully.")
            return redirect("/customer")
        else:
            messages.error(request, "The two passwords do not match.")
            return redirect("/customer/reset-password/" + user.encrypted_id + "/")


def vendorAccount(request):
    return render(request, "E_Commerce/Login_Registration_Vendor.html")


def login_vendor(request):
    if request.method == "POST":
        u_name = request.POST["u_name"]
        password_login = request.POST["password_login"]
        user = Vendor()
        try:
            if user.login(u_name, password_login):
                request.session["authenticated"] = True
                return HttpResponse("SUCCESS")
            else:
                messages.error(request, "Invalid Username/Password")
                return redirect("/vendor")
        except AssertionError:
            if "@" in u_name:
                i = u_name.index("@")
                username = u_name[:i]
            else:
                username = u_name
            messages.info(request,
                          "Verify your email. <a href='activation_email/vendor/" + username + "/'>Resend</a> verification email")
            return redirect("/vendor")
        except Vendor.DoesNotExist:
            messages.error(request, "Invalid Username/Password")
            return redirect("/vendor")


def signup_vendor(request):
    if request.method == "POST":
        email = request.POST["email"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        password = request.POST["Password"]
        confirm_password = request.POST["ConfirmPassword"]
        contact_number = request.POST["contact_number"]
        try:
            if password == confirm_password:
                user = Vendor()
                user.create_Vendor(email, firstname, lastname, contact_number, make_password(password))
                user.sendEmail(user, request)
                messages.info(request, "Account Created Successfully. Verify your email.")
                return redirect("/vendor")
            else:
                messages.error(request, "Error: Password does not match.")
                return redirect("/vendor")
        except MultiValueDictKeyError:
            return redirect("/vendor")
        except TypeError:
            messages.error(request, "Invalid First or Last Name")
            return redirect("/vendor")
        except IntegrityError:
            messages.error(request, "You are already signed up.")
            return redirect("/vendor")
        except ValueError:
            messages.error(request, "Invalid Contact Number")
            return redirect("/vendor")
    else:
        return HttpResponse("404 not Found")


def activation_email_vendor(request, username):
    user = Vendor.objects.get(username=username)
    user.sendEmail(user, request)
    messages.info(request, "Email sent! If you can't find the email, check your spam")
    return redirect("/vendor")


def activate_vendor(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Vendor.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        return HttpResponse("404 Error")
    if user is not None and account_activation_token.check_token(user, token):
        user.verified = True
        request.session["authenticated"] = True
        user.save()
        return render(request, 'E_Commerce/Welcome.html')
    else:
        return HttpResponse('Activation link is invalid!')


def lost_password_vendor(request):
    return render(request, "E_Commerce/LostPasswordVendor.html")


def lost_password_email_vendor(request):
    if request.method == "POST":
        name_email = request.POST["u_name_email"]
        if "@" in name_email:
            i = name_email.index("@")
            username = name_email[:i]
        else:
            username = name_email
        try:
            user = Vendor.objects.get(username=username)
            user.sendPasswordResetEmail(request, user)
            messages.info(request, "Password Reset Email Sent.")
            return redirect("/vendor/lost-password")
        except Vendor.DoesNotExist:
            messages.error(request, "No such customer exist.")
            return redirect("/vendor/lost-password")


def password_reset_vendor(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Vendor.objects.get(pk=uid)
        enc_id = user.encrypted_id
        if user is not None and password_reset_token.check_token(user, token):
            return redirect("/vendor/reset-password-vendor/" + enc_id + "/")
        else:
            return HttpResponse('Reset password link is invalid!')
    except(TypeError, ValueError, OverflowError, Vendor.DoesNotExist):
        return HttpResponse('Reset password link is invalid!')


def reset_password_vendor(request, enc_id):
    return render(request, 'E_Commerce/ResetPasswordVendor.html')


def new_password_vendor(request, enc_id):
    user = Vendor.objects.get(encrypted_id=enc_id)
    if request.method == "POST":
        password = request.POST["newPass"]
        c_password = request.POST["newPassConfirm"]
        if password == c_password:
            user.password = make_password(password)
            user.save()
            messages.success(request, "Password changed successfully.")
            return redirect("/vendor")
        else:
            messages.error(request, "The two passwords do not match.")
            return redirect("/vendor/reset-password-vendor/" + user.encrypted_id + "/")


def logout(request):
    if request.session.has_key("authenticated"):
        del request.session["authenticated"]
    return redirect("/")


def temp(request):
    return render(request, "E_Commerce/Welcome.html")