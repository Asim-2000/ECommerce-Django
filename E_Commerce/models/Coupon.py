import random
import string

from django.db import models
from django_extensions.db.models import TimeStampedModel
from E_Commerce.models import Vendor


class Coupon(TimeStampedModel):
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=100)
    percent_off = models.IntegerField()
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)

    def add_coupon(self,vendor, name, percent_off):
        self.name = name
        self.vendor = vendor
        self.percent_off = percent_off
        self.number = self.get_random_string()
        self.save()

    def get_random_string(self):
        result_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return result_str
