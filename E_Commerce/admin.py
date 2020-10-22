from django.contrib import admin

# Register your models here.

from .models import Customer,Vendor, Review, Product

admin.site.register(Customer)
admin.site.register(Vendor)
admin.site.register(Review)
admin.site.register(Product)