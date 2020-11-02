from django.conf import settings
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
        Always_Accessible = ["", "cart", "temp"]
        Allowed_urls = ['activate', 'password_reset', 'customer/emailpassword', \
                        'customer/lost-password', 'customer/reset-password',
                        'vendor/vendorpassword', 'vendor/lost-password',
                        'vendor/reset-password']
        path = request.path_info.lstrip('/')
        url_accessible = any(url == path for url in Always_Accessible)
        url_is_exempt = any(url == path for url in Exempt_url)
        allow_these_urls = any(path.startswith(url) for url in Allowed_urls)

        if url_accessible:
            return None
        elif request.session.has_key('authenticated') and url_is_exempt:
            return render(request, "E_Commerce/Profile.html")
        elif request.session.has_key('authenticated') or url_is_exempt or allow_these_urls:
            return None
        elif path == "vendor":
            return redirect('/vendor')
        else:
            messages.warning(request, "Login to Continue")
            return redirect('/customer')
