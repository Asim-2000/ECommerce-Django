from django.db import models
from django_extensions.db.models import TimeStampedModel
from E_Commerce.models import Product


class Image(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/")