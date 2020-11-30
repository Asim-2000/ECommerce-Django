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
    path('vendor_account_details', views.account_details),
    path('rma-requests', views.rma_requests),
    path('vendors_page', views.vendors),
    path('tickets', views.tickets),
    path('password_reset/<uidb64>/<token>/', views.password_reset, name='password_reset'),
    path('customer/reset-password/<enc_id>/new-password', views.new_password),
    path('vendor', views.vendor_account),
    path('login-vendor', views.login_vendor),
    path('signup-vendor', views.signup_vendor),
    path('activation_email/vendor/<username>/', views.activation_email_vendor),
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
    path('new-product', views.new_product),
    path('dashboard-vendor', views.dashboard_vendor),
    path('orders-vendor', views.orders_vendor),
    path('profile', views.profile),
    path('update_vendor', views.update_vendor),
    path('update_customer', views.update_customer),
    path('create_product', views.create_product),
    path('account_details_customer', views.account_details_customer),
    path('vendor_coupons', views.vendor_coupons),
    path('edit_product', views.edit_product),
    path('reports_vendor', views.reports_vendor),
    path('reviews_vendor', views.reviews_vendor),
    path('withdraw_vendor', views.withdraw_vendor),
    path('returns_vendor', views.returns_vendor),
    path('staff_vendor', views.staff_vendor),
    path('add_staff', views.add_staff),
    path('followers_vendor', views.followers_vendor),
    path('tools_vendor', views.tools_vendor),
    path('support_tickets_vendor', views.support_tickets_vendor),
    path('request-category', views.request_category),
    path('tag-create', views.tag_create),
    path('add_to_cart/<prod_pk>', views.add_to_cart)

]
