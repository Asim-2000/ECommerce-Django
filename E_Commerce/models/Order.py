from django.db import models
from django_extensions.db.models import TimeStampedModel
from E_Commerce.models import Customer, Address


class Order(TimeStampedModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    payment_mode = models.CharField(max_length=50)
