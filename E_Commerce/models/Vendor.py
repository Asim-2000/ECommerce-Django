from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django_extensions.db.models import TimeStampedModel

from E_Commerce.tokens import account_activation_token


class Vendor(TimeStampedModel):
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    email = models.EmailField(unique=True, null=True)
    password = models.CharField(max_length=30)
    contact_number = models.CharField(max_length=30)
    featured = models.BooleanField(verbose_name='featured', default=False)
    verified = models.BooleanField(verbose_name='verified', default=False)

    def create_Vendor(self, email, firstname, lastname, contact_number, password):
        self.email = email
        self.firstname = self.set_name(firstname)
        self.lastname = self.set_name(lastname)
        self.password = password
        self.set_contact_number(contact_number)
        self.featured = False
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

    def sendEmail(self,user, request):
        current_site = get_current_site(request)
        mail_subject = 'Activate your account.'
        message = render_to_string('E_Commerce/Activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        send_mail(mail_subject, message, 'noreply@karkhanay.com', [user.email],
                  fail_silently=False, )
