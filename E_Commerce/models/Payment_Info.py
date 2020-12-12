from django.db import models
from django_extensions.db.models import TimeStampedModel

from E_Commerce.models import Vendor


class Payment_Info(TimeStampedModel):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    accountname = models.CharField(max_length=80)
    accountno = models.CharField(max_length=30)
    bankname = models.CharField(max_length=50)
    iban = models.BooleanField(verbose_name="International Banking", default=False)
    bank_streetaddress = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    zipcode = models.CharField(max_length=20)
    country = models.CharField(max_length=30)