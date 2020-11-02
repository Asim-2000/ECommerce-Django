from django.db import models
from E_Commerce.models.User import User


class Vendor(User):
    featured = models.BooleanField(verbose_name='featured', default=False)

    def create_Vendor(self, email, firstname, lastname, contact_number, password):
        self.email = email
        self.firstname = self.set_name(firstname)
        self.lastname = self.set_name(lastname)
        self.password = password
        self.set_contact_number(contact_number)
        self.featured = False
        self.verified = False
        self.username = self.generate_username(email)
        self.encrypted_id = self.get_random_string()
        self.save()
