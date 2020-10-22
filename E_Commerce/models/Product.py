from django.db import models
from django_extensions.db.models import TimeStampedModel
from E_Commerce.models import Store, Tag

class Product(TimeStampedModel):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    price = models.FloatField(max_length=100)
    description = models.CharField(max_length=1000)
    stock_count = models.IntegerField()
    featured = models.BooleanField(verbose_name='featured_product', default=False)
    tag = models.ManyToManyField(Tag)