from django.contrib import messages
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.cache import cache_control

from .models import Customer, Vendor, Store, Product_Category, Tag, Image, Product, Cart
from django.http import HttpResponse, JsonResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.hashers import make_password, check_password

# Create your views here.
from .tokens import account_activation_token, password_reset_token

temp_cart = []


def home(request):
    prod = Product.objects.all()
    ven = {
        "prod": prod
    }
    return render(request, 'E_Commerce/DisplayProduct.html', ven)


def account(request):
    return render(request, 'E_Commerce/Login_Registration.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def cart(request):
    if request.session.has_key("product"):
        temp = request.session["product"]
        ls = []
        for p in temp:
            product = Product.objects.get(pk=p)
            if product not in ls:
                ls.append(product)
        ven = {
            "product": ls
        }
        return render(request, 'E_Commerce/Cart.html', ven)
    return render(request, 'E_Commerce/Cart.html')


def checkout(request):
    if request.method == "POST":
        if request.session.has_key("product"):
            temp = request.session["product"]
            ls = []
            prod = []
            quan = []
            total = 0
            for p in temp:
                product = Product.objects.get(pk=p)
                quantity = request.POST["quantity" + p]
                prod.append(product)
                quan.append(quantity)
                total += product.price * int(quantity)

            zipped = zip(prod, quan)
            ven = {
                "zipped": zipped, "total": total
            }
            return render(request, "E_Commerce/Checkout.html", ven)


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
    return render(request, 'E_Commerce/VendorAccountDetails.html', ven)


def rma_requests(request):
    return render(request, 'E_Commerce/RMA_Requests.html')


def vendors(request):
    return render(request, 'E_Commerce/DashboardVendor.html')


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
            logged_in_user = user.login(u_name, password_login)
            if logged_in_user is not None:
                request.session["authenticated"] = logged_in_user.encrypted_id
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
    return render(request, "E_Commerce/Checkout.html")


def products(request):
    return render(request, "E_Commerce/Products.html")


def new_product(request):
    categories = Product_Category.objects.all()
    tags = Tag.objects.all()
    cat = {
        "categories": categories,
        "tags": tags
    }
    return render(request, "E_Commerce/AddProducts.html", cat)


def dashboard_vendor(request):
    return render(request, "E_Commerce/DashboardVendor.html")


def orders_vendor(request):
    return render(request, 'E_Commerce/OrdersVendor.html')


def account_details_customer(request):
    enc_id = request.session["authenticated"]
    user = Customer.objects.get(encrypted_id=enc_id)
    ven = {
        "user": user
    }
    return render(request, 'E_Commerce/AccountDetails.html', ven)


def vendor_coupons(request):
    return render(request, 'E_Commerce/VendorCoupons.html')


def reports_vendor(request):
    return render(request, 'E_Commerce/ReportsVendor.html')


def reviews_vendor(request):
    return render(request, 'E_Commerce/ReviewsVendor.html')


def withdraw_vendor(request):
    return render(request, 'E_Commerce/WithdrawVendor.html')


def returns_vendor(request):
    return render(request, 'E_Commerce/ReturnsVendor.html')


def staff_vendor(request):
    return render(request, 'E_Commerce/StaffVendor.html')


def add_staff(request):
    return render(request, 'E_Commerce/AddStaff.html')


def followers_vendor(request):
    return render(request, 'E_Commerce/FollowersVendor.html')


def tools_vendor(request):
    return render(request, 'E_Commerce/ToolsVendor.html')


def support_tickets_vendor(request):
    return render(request, 'E_Commerce/SupportVendor.html')


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
    return render(request, "E_Commerce/Profile.html")


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
            user.username = user.generate_username(email)
            user.save()
        except Vendor.DoesNotExist:
            return HttpResponse("404 Error")
        if request.POST["c_password"] != "" and check_password(request.POST["c_password"], user.password):
            if request.POST["n_password"] == request.POST["cnfm_password"]:
                user.password = make_password(request.POST["n_password"])
                user.save()
            else:
                messages.error(request, "The two passwords does not match")
                return redirect("/vendor_account_details")
        elif request.POST["c_password"] != "" and not check_password(request.POST["c_password"], user.password):
            messages.error(request, "The current password is not correct")
            return redirect("/vendor_account_details")

        messages.success(request, "Profile Updated")
        return redirect("/vendor_account_details")


def create_product(request):
    if request.method == "POST":
        prod = Product()
        user = Vendor.objects.get(encrypted_id=request.session["authenticated"])
        store = Store.objects.get(vendor=user)

        name = request.POST["ProductName"]
        price = request.POST["price"]
        discounted = request.POST["discount"]
        s_des = request.POST["shortDescription"]
        des = request.POST["description"]
        category = Product_Category.objects.get(name=request.POST["categories"])
        tag = request.POST.getlist("tags")
        stock_count = request.POST["stock_count"]
        prod.create_product(store, name, category, price, discounted, des, s_des, stock_count)

        tags = []
        for t in tag:
            tags.append(Tag.objects.get(name=t))

        prod.tag.set(tags)
        prod.featured_image = request.FILES.getlist("images")[0]
        prod.save()
        for file in request.FILES.getlist("images"):
            img = Image()
            img.image = file
            img.product = prod
            img.save()

        request.session["product"] = prod.pk
        return render(request, 'E_Commerce/EditProduct.html')


def edit_product(request):
    pd_id = request.session["product"]
    product = Product.objects.get(pk=pd_id)
    if request.method == "POST":
        # product.name = request.POST["Title"]
        # product.price = request.POST["price"]
        # product.discounted_price = request.POST["discount"]
        # category = Product_Category.objects.get(name=request.POST["categories"])
        # tag = request.POST.getlist("tags")
        # product.product_category = category
        # product.short_description = request.POST["shortDescription"]
        # product.description = request.POST["description"]
        # tags = []
        # for t in tag:
        #    tags.append(Tag.objects.get(name=t))

        # product.tag.set(tags)
        product.sku = request.POST["sku"]
        product.stock_status = request.POST["status"]
        product.one_quantity_sale = request.POST["one_quantity"] == "on"
        product.stock_management = request.POST["stock_management"] == "on"
        product.weight = request.POST["weight"]
        product.status = request.POST["productStatus"]
        product.visibility = request.POST["visibility"]
        product.purchase_note = request.POST["purchaseNote"]
        product.save()
        messages.success(request, "Product Created Successfully!")

        del request.session["product"]
        return redirect("/products")


def update_customer(request):
    if request.method == "POST":
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        email = request.POST["email"]
        try:
            user = Customer.objects.get(encrypted_id=request.session["authenticated"])
            user.firstname = firstname
            user.lastname = lastname
            user.email = email
            user.username = user.generate_username(email)
            user.save()
        except Customer.DoesNotExist:
            return HttpResponse("404 Error")
        if request.POST["c_password"] != "" and check_password(request.POST["c_password"], user.password):
            if request.POST["n_password"] == request.POST["cnfm_password"]:
                user.password = make_password(request.POST["n_password"])
                user.save()
            else:
                messages.error(request, "The two passwords does not match")
                return redirect("/account_details_customer")
        elif request.POST["c_password"] != "" and not check_password(request.POST["c_password"], user.password):
            messages.error(request, "The current password is not correct")
            return redirect("/account_details_customer")

        messages.success(request, "Profile Updated")
        return redirect("/account_details_customer")


def request_category(request):
    if request.method == "POST":
        name = request.POST["category-name"]
        des = request.POST["des"]
        mail_subject = 'Vendor has requested a Category'
        message = render_to_string('E_Commerce/Request_Category_Email.html', {
            'name': name,
            'des': des,
        })
        send_mail(mail_subject, message, 'noreply@karkhanay.com', ['fahadzaheer19@gmail.com'],
                  fail_silently=False)
        messages.success(request, "Category Requested.")
        return redirect('/dashboard-vendor')


def tag_create(request):
    if request.method == "POST":
        name = request.POST["tag-name"]
        tag_des = request.POST["tag-description"]
        slug = request.POST['slug']

        tag = Tag()
        tag.name = name
        tag.description = tag_des
        tag.slug = slug
        tag.save()
        messages.success(request, "Tag created successfully.")
        return redirect("/dashboard-vendor")


def add_to_cart(request, prod_pk):
    temp_cart.append(prod_pk)
    request.session["product"] = temp_cart
    return redirect("/")
