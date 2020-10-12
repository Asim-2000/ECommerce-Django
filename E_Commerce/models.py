from django.db import models
from django_extensions.db.models import TimeStampedModel


# Create your models here.
class Customer(TimeStampedModel):
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    username = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=30)
    contact_number = models.CharField(max_length=30)


class Vendor(TimeStampedModel):
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=30)
    contact_number = models.CharField(max_length=30)
    featured = models.BooleanField(verbose_name='featured', default=False)
    approved = models.BooleanField(verbose_name='verified', default=False)


class Store(TimeStampedModel):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=1000)
    banner = models.CharField(max_length=50)
    street_address = models.CharField(max_length=30)
    zipcode = models.CharField(max_length=10)
    state = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    store_opening_time = models.TimeField(auto_now=False, auto_now_add=False)
    store_closing_time = models.TimeField(auto_now=False, auto_now_add=False)