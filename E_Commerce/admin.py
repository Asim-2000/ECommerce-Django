from django.contrib import admin

# Register your models here.

from .models import CUSTOMER,VENDOR, REVIEW, PRODUCT

admin.site.register(CUSTOMER)
admin.site.register(VENDOR)
admin.site.register(REVIEW)
admin.site.register(PRODUCT)