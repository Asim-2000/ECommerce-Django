from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import render, redirect, render_to_response
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from .models import Customer, Vendor, Store
from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.hashers import make_password, check_password

# Create your views here.
from .tokens import account_activation_token, password_reset_token


def home(request):
    return render(request, 'E_Commerce/HomePage.html')


def account(request):
    return render(request, 'E_Commerce/Login_Registration.html')


def cart(request):
    return render(request, 'E_Commerce/Cart.html')


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
    enc_id = request.session["authenticated"]
    user = Vendor.objects.get(encrypted_id=enc_id)
    ven = {
        "user": user
    }
    return render(request, 'E_Commerce/AccountDetails.html', ven)


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
                user.create_customer(firstname, lastname, email, make_password(password), contact_number)
                user.sendemail(user, request)
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
        except Customer.DoesNotExist:
            messages.error(request, "Invalid Username/Password")
            return redirect("/customer")


def activation_email(request, username):
    user = Customer.objects.get(username=username)
    user.sendemail(user, request)
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


def vendor_account(request):
    return render(request, "E_Commerce/Login_Registration_Vendor.html")


def login_vendor(request):
    if request.method == "POST":
        u_name = request.POST["u_name"]
        password_login = request.POST["password_login"]
        user = Vendor()
        try:
            logged_in_user = user.login(u_name, password_login)
            if logged_in_user is not None:
                request.session["authenticated"] = logged_in_user.encrypted_id
                return redirect("/vendors_page")
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
                user.create_vendor(email, firstname, lastname, contact_number, make_password(password))
                user.sendemail(user, request)
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
    user.sendemail(user, request)
    messages.info(request, "Email sent! If you can't find the email, check your spam")
    return redirect("/vendor")


def activate_vendor(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Vendor.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Vendor.DoesNotExist):
        return HttpResponse("404 Error")
    if user is not None and account_activation_token.check_token(user, token):
        user.verified = True
        request.session["authenticated"] = user.encrypted_id
        user.save()
        return redirect("/store_registration_page")
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


def store_registration(request):
    if request.method == "POST":
        store_name = request.POST["StoreName"]
        store_url = request.POST["StoreURL"]
        store = Store()
        enc_id = request.session["authenticated"]
        user = Vendor.objects.get(encrypted_id=enc_id)
        try:
            if user is not None:
                store.create_store(store_name, store_url, user)
            return render(request, "E_Commerce/StoreSetup.html")
        except IntegrityError:
            messages.error(request, "Change the URL of your store")
            return redirect("/store_registration_page")


def temp(request):
    return render(request, "E_Commerce/temp.html")


def products(request):
    return render(request, "E_Commerce/Products.html")


def new_product(request):
    return render(request, "E_Commerce/AddProducts.html")


def dashboard_vendor(request):
    return render(request, "E_Commerce/DashboardVendor.html")


def orders_vendor(request):
    return render(request, 'E_Commerce/OrdersVendor.html')


def store_setup(request):
    if request.method == "POST":
        user = Vendor.objects.get(encrypted_id=request.session["authenticated"])
        try:
            store = Store.objects.get(vendor=user)
            store.product_per_page = request.POST["products"]
            store.street_address = request.POST["street"] + " " + request.POST["street2"]
            store.city = request.POST["city"]
            store.zipcode = request.POST["zipcode"]
            store.state = request.POST["state"]
            store.country = request.POST["Country"]
            store.show_email = (request.POST["defaultCheck1"] == 'on')
            store.save()
            return render(request, "E_Commerce/PaymentSetup.html")
        except Store.DoesNotExist:
            return HttpResponse("Error 404!")


def store_register_page(request):
    return render(request, 'E_Commerce/StoreRegistration.html')


def profile(request):
    enc_id = request.session["authenticated"]
    user = Vendor.objects.get(encrypted_id=enc_id)
    ven = {
        "vendor": user
    }
    return render(request, "E_Commerce/Profile.html", ven)


def update_vendor(request):
    if request.method == "POST":
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        email = request.POST["email"]
        try:
            user = Vendor.objects.get(encrypted_id=request.session["authenticated"])
            user.firstname = firstname
            user.lastname = lastname
            user.email = email
            user.save()
        except Vendor.DoesNotExist:
            return HttpResponse("404 Error")
        if request.POST["c_password"] is not "" and check_password(request.POST["c_password"], user.password):
            if request.POST["n_password"] == request.POST["cnfm_password"]:
                user.password = make_password(request.POST["n_password"])
                user.save()
            else:
                messages.error(request, "The two passwords does not match")
                return redirect("/account-details")
        elif request.POST["c_password"] is not "" and not check_password(request.POST["c_password"], user.password):
            messages.error(request, "The current password is not correct")
            return redirect("/account-details")

        messages.success(request, "Profile Updated")
        return redirect("/account-details")