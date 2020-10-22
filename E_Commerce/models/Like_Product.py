from django.db import models
from django_extensions.db.models import TimeStampedModel
from E_Commerce.models import Product, Customer


class Like_Product(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
