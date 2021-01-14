from django.db import models
from django_extensions.db.models import TimeStampedModel
from E_Commerce.models import Customer


class Address(TimeStampedModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    streetaddress = models.CharField(max_length=1000, null=False)
    city = models.CharField(max_length=30, null=False)
    state = models.CharField(max_length=30, null=False)
    zipcode = models.CharField(max_length=20, null=False)
    country = models.CharField(max_length=30, null=False)

    def createAddress(self, customer, st_adress, city, state, zipcode, country):
        self.customer = self.notEmpty(customer)
        self.streetaddress = self.notEmpty(st_adress)
        self.city = self.notEmpty(city)
        self.country = self.notEmpty(country)
        self.state = self.notEmpty(state)
        self.zipcode = self.notEmpty(zipcode)
        self.save()

    def tostr(self):
        return self.streetaddress + " " + self.city

    def notEmpty(self, parameter):
        if parameter != "":
            return parameter
        raise TypeError

