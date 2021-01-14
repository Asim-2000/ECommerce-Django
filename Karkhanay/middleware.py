from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        Exempt_url = ["customer", "vendor", "login", "signup", "signup-vendor", "login-vendor"]
        Always_Accessible = ["", "cart", "temp",  "logout", 'wishlist',]
        Allowed_urls = ['activate', 'password_reset', 'customer/emailpassword',
                        'activation_email', 'product_category',
                        'customer/lost-password', 'customer/reset-password',
                        'vendor/vendorpassword', 'vendor/lost-password',
                        'vendor/reset-password', "admin", "add_to_cart", "media/",
                         'single_product','inquire']

        Customer_urls = ['addresses', 'checkout', 'place_order',
                         'profile', "add_to_wishlist", 'review', 'account_details_customer',
                         'update_customer', 'addresses', 'tickets', 'customer']

        path = request.path_info.lstrip('/')
        url_accessible = any(url == path for url in Always_Accessible)
        url_is_exempt = any(url == path for url in Exempt_url)
        allow_these_urls = any(path.startswith(url) for url in Allowed_urls)
        customer_urls = any(path.startswith(url) for url in Customer_urls)
        if url_accessible or allow_these_urls:
            return None
        elif request.session.has_key('customer') and url_is_exempt:
            return redirect("/customer_panel")
        elif request.session.has_key('customer') and not customer_urls:
            messages.warning(request, "These pages are only for vendor")
            return redirect("/customer_panel")
        elif request.session.has_key('customer') and customer_urls:
            return None
        elif request.session.has_key('authenticated') and url_is_exempt:
            return redirect("/dashboard-vendor")
        elif (request.session.has_key('authenticated') and not customer_urls) or url_is_exempt:
            return None
        elif request.session.has_key('authenticated') and customer_urls:
            messages.warning(request, "These pages are only for customer")
            return redirect("/dashboard-vendor")
        else:
            messages.warning(request, "Login to Continue")
            return redirect('/customer')

