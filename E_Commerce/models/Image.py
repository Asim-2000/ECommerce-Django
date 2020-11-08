from django.db import models
from django_extensions.db.models import TimeStampedModel
from E_Commerce.models import Product


class Image(TimeStampedModel):
    image = models.ImageField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def image(self, image, product):
        self.image = image
        self.product = product
        self.save()