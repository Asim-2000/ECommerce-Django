from django.db import models
from django_extensions.db.models import TimeStampedModel


# Create your models here.
class CUSTOMER(TimeStampedModel):
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    username = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=30)
    contact_number = models.CharField(max_length=30)

    def __str__(self):
        return self.username


class VENDOR(TimeStampedModel):
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=30)
    contact_number = models.CharField(max_length=30)
    featured = models.BooleanField(verbose_name='featured', default=False)
    approved = models.BooleanField(verbose_name='verified', default=False)


class STORE(TimeStampedModel):
    vendor = models.ForeignKey(VENDOR, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=1000)
    banner = models.CharField(max_length=50)
    street_address = models.CharField(max_length=30)
    zipcode = models.CharField(max_length=10)
    state = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    store_opening_time = models.TimeField(auto_now=False, auto_now_add=False)
    store_closing_time = models.TimeField(auto_now=False, auto_now_add=False)


class PAYMENT_INFO(TimeStampedModel):
    vendor = models.ForeignKey(VENDOR, on_delete=models.CASCADE)
    accountname = models.CharField(max_length=80)
    accountno = models.CharField(max_length=30)
    bankname = models.CharField(max_length=50)
    iban = models.BooleanField(verbose_name="International Banking", default=False)
    bank_streetaddress = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    zipcode = models.CharField(max_length=20)
    country = models.CharField(max_length=30)


class ADDRESS(TimeStampedModel):
    customer = models.ForeignKey(CUSTOMER, on_delete=models.CASCADE)
    streetaddress = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    zipcode = models.CharField(max_length=20)
    country = models.CharField(max_length=30)


class ORDER(TimeStampedModel):
    customer = models.ForeignKey(CUSTOMER, on_delete=models.CASCADE)
    address = models.ForeignKey(ADDRESS, on_delete=models.CASCADE)
    payment_mode = models.CharField(max_length=50)


class STORE_FOLLOWER(TimeStampedModel):
    store = models.ForeignKey(STORE, on_delete=models.CASCADE)
    customer = models.ForeignKey(CUSTOMER, on_delete=models.CASCADE)


class TAG(TimeStampedModel):
    name = models.CharField(max_length=30)
    slug = models.CharField(max_length=30)
    description = models.CharField(max_length=500)


class PRODUCT(TimeStampedModel):
    store = models.ForeignKey(STORE, on_delete=models.CASCADE)
    price = models.FloatField(max_length=100)
    description = models.CharField(max_length=1000)
    stock_count = models.IntegerField()
    featured = models.BooleanField(verbose_name='featured_product', default=False)
    tag = models.ManyToManyField(TAG)


class REVIEW(TimeStampedModel):
    STARS = (
        ('1 star', '*'),
        ('2 star', '**'),
        ('3 star', '***'),
        ('4 star', '****'),
        ('5 star', '*****'),
    )
    rating = models.IntegerField(choices=STARS)
    description = models.CharField(max_length=1000)
    product = models.ForeignKey(PRODUCT, on_delete=models.CASCADE)
    customer = models.ForeignKey(CUSTOMER, on_delete=models.CASCADE)


class ORDER_DETAIL(TimeStampedModel):
    product = models.ForeignKey(PRODUCT, on_delete=models.CASCADE)
    order = models.ForeignKey(ORDER, on_delete=models.CASCADE)
    quantity = models.IntegerField()


class CART(TimeStampedModel):
    product = models.ForeignKey(PRODUCT, on_delete=models.CASCADE)
    customer = models.ForeignKey(CUSTOMER, on_delete=models.CASCADE)


class WISHLIST(TimeStampedModel):
    product = models.ForeignKey(PRODUCT, on_delete=models.CASCADE)
    customer = models.ForeignKey(CUSTOMER, on_delete=models.CASCADE)


class LIKE_PRODUCT(TimeStampedModel):
    product = models.ForeignKey(PRODUCT, on_delete=models.CASCADE)
    customer = models.ForeignKey(CUSTOMER, on_delete=models.CASCADE)


class IMAGE(TimeStampedModel):
    product = models.ForeignKey(PRODUCT, on_delete=models.CASCADE)

# SALE and PRODUCT_CATEGORY models yet to be completed. Waiting for them to be finalized
