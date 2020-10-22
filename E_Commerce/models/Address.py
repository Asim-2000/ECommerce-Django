from django.db import models
from django_extensions.db.models import TimeStampedModel
from E_Commerce.models import Customer


class Address(TimeStampedModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    streetaddress = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    zipcode = models.CharField(max_length=20)
    country = models.CharField(max_length=30)
