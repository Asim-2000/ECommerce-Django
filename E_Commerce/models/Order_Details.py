from django.db import models
from django_extensions.db.models import TimeStampedModel
from E_Commerce.models import Product, Order


class Order_Detail(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField()
