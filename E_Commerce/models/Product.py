from django.db import models
from django_extensions.db.models import TimeStampedModel
from E_Commerce.models import Store, Tag, Product_Category


class Product(TimeStampedModel):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    product_category = models.ForeignKey(Product_Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.FloatField(max_length=100)
    discounted_price = models.FloatField(max_length=100)
    short_description = models.CharField(max_length=500, null=True)
    description = models.CharField(max_length=1000)
    stock_count = models.IntegerField(null=True)
    featured = models.BooleanField(verbose_name='featured_product', default=False)
    tag = models.ManyToManyField(Tag)
    stock_status = models.CharField(max_length=20)
    one_quantity_sale = models.BooleanField(verbose_name="one_quantity_name", default=False)
    stock_management = models.BooleanField(verbose_name="stock_management", default=False)
    weight = models.FloatField(max_length=10, null=True)
    sku = models.CharField(max_length=50, null=True)
    status = models.CharField(max_length=50, null=True)
    visibility = models.CharField(max_length=50, null=True)
    purchase_note = models.CharField(max_length=100,null=True)
    featured_image = models.ImageField(upload_to="products/")

    def create_product(self, store, name, category, price, discounted_price, description, s_description, stk_cnt):
        self.name = name
        self.product_category = category
        self.price = price
        self.description = description
        self.discounted_price = discounted_price
        self.short_description = s_description
        self.stock_count = stk_cnt
        self.store = store
        self.save()

