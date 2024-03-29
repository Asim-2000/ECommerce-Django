from django.db import models
from django_extensions.db.models import TimeStampedModel
from E_Commerce.models import Vendor


class Store(TimeStampedModel):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=1000)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    banner = models.CharField(max_length=50)
    url = models.URLField(unique=True)
    street_address = models.CharField(max_length=300)
    zipcode = models.CharField(max_length=10)
    state = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    product_per_page = models.IntegerField(null=True)
    store_opening_time = models.TimeField(auto_now=False, auto_now_add=False, null=True)
    store_closing_time = models.TimeField(auto_now=False, auto_now_add=False, null=True)
    show_email = models.BooleanField(default=False, null=True)

    def create_store(self, name, url, vendor):
        self.name = name
        self.url = url
        self.vendor = vendor
        self.save()