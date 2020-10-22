from django.db import models
from django_extensions.db.models import TimeStampedModel
from E_Commerce.models import Product, Customer


class Review(TimeStampedModel):
    STARS = (
        ('1 star', '*'),
        ('2 star', '**'),
        ('3 star', '***'),
        ('4 star', '****'),
        ('5 star', '*****'),
    )
    rating = models.IntegerField(choices=STARS)
    description = models.CharField(max_length=1000)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
