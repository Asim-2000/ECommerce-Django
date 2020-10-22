from django.db import models
from django_extensions.db.models import TimeStampedModel


class Customer(TimeStampedModel):
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    contact_number = models.CharField(max_length=30)
    verified = models.BooleanField(verbose_name='verified', default=False)

    def generate_username(self, email="123@gmail.com"):
        i = email.index("@")
        username = email[:i]
        return username

    def __str__(self):
        return self.username

    def create_Customer(self, firstname, lastname, email, password, contact_number):
        self.firstname = self.set_name(firstname)
        self.lastname = self.set_name(lastname)
        self.email = email
        self.password = password
        self.username = self.generate_username(email)
        self.set_contact_number(contact_number)
        self.verified = False
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
