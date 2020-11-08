from django.db import models
from django_extensions.db.models import TimeStampedModel
from E_Commerce.models import Store, Tag, Product_Category, Image


class Product(TimeStampedModel):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    product_category = models.ForeignKey(Product_Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.FloatField(max_length=100)
    discounted_price = models.FloatField(max_length=100)
    description = models.CharField(max_length=1000)
    stock_count = models.IntegerField()
    featured = models.BooleanField(verbose_name='featured_product', default=False)
    tag = models.ManyToManyField(Tag)

    def create_product(self, name, category, tag, price, discounted_price, description, image):
        self.name = name
        self.product_category = category
        self.tag = tag
        self.price = price
        self.description = description
        self.discounted_price = discounted_price
        i = Image()
        i.image(image, self)
        self.save()
