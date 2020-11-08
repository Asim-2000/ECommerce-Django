from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, ),
    path('customer', views.account),
    path('signup', views.signup),
    path('cart', views.cart),
    path('paymentsetup', views.payment_setup),
    path('ready', views.ready),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('login', views.login),
    path('activation_email/<username>/', views.activation_email),
    path('customer/lost-password', views.lost_password),
    path('customer/emailpassword', views.lost_password_email),
    path('customer/reset-password/<enc_id>/', views.reset_password),
    path('orders', views.orders),
    path('downloads', views.downloads),
    path('addresses', views.addresses),
    path('account-details', views.account_details),
    path('rma-requests', views.rma_requests),
    path('vendors_page', views.vendors),
    path('tickets', views.tickets),
    path('password_reset/<uidb64>/<token>/', views.password_reset, name='password_reset'),
    path('customer/reset-password/<enc_id>/new-password', views.new_password),
    path('vendor', views.vendor_account),
    path('login-vendor', views.login_vendor),
    path('signup-vendor', views.signup_vendor),
    path('activation_email/<username>/', views.activation_email_vendor),
    path('activate_vendor/<uidb64>/<token>/', views.activate_vendor, name='activate_vendor'),
    path('vendor/lost-password', views.lost_password_vendor),
    path('vendor/vendorpassword', views.lost_password_email_vendor),
    path('password_reset_vendor/<uidb64>/<token>/', views.password_reset_vendor, name='password_reset_vendor'),
    path('vendor/reset-password-vendor/<enc_id>/', views.reset_password_vendor),
    path('vendor/reset-password-vendor/<enc_id>/new-password-vendor', views.new_password_vendor),
    path('store-registration', views.store_registration),
    path('logout', views.logout),
    path('temp', views.temp),
    path('store-setup', views.store_setup),
    path('store_registration_page', views.store_register_page),
    path('products', views.products),
    path('products/new-product', views.new_product),
    path('dashboard-vendor', views.dashboard_vendor),
    path('orders-vendor', views.orders_vendor),

]
