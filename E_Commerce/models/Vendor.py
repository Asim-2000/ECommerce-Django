from django.db import models
from django_extensions.db.models import TimeStampedModel


class Vendor(TimeStampedModel):
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    email = models.EmailField(unique=True, null=True)
    password = models.CharField(max_length=30)
    contact_number = models.CharField(max_length=30)
    featured = models.BooleanField(verbose_name='featured', default=False)
    approved = models.BooleanField(verbose_name='verified', default=False)

    def create_Vendor(self, email, firstname, lastname, contact_number, password):
        self.email = email
        self.firstname = self.set_name(firstname)
        self.lastname = self.set_name(lastname)
        self.password = password
        self.set_contact_number(contact_number)
        self.featured = False
        self.approved = False
        self.save()

    def set_contact_number(self, contactNumber):
        if not contactNumber.isdecimal() or not len(contactNumber) == 10:
            raise ValueError
        self.contact_number = contactNumber

    def set_name(self, name):
        for char in name:
            if char.isdigit():
                raise TypeError
        return name
