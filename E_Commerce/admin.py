from django.contrib import admin

# Register your models here.

from .models import Customer,Vendor, Product_Category, Product

admin.site.register(Customer)
admin.site.register(Vendor)
admin.site.register(Product_Category)
admin.site.register(Product)