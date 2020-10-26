from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django_extensions.db.models import TimeStampedModel
from django.contrib.auth.hashers import check_password

from E_Commerce.tokens import account_activation_token, password_reset_token


class Customer(TimeStampedModel):
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=500)
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

    def login(self, username, password):
        u_name = username
        if "@" in username:
            u_name = self.generate_username(username)
        session = Customer.objects.get(username=u_name)
        if check_password(password, session.password):
            if session.verified:
                return True
            else:
                raise AssertionError
        else:
            return False

    def sendEmail(self, user, request):
        current_site = get_current_site(request)
        mail_subject = 'Activate your account.'
        message = render_to_string('E_Commerce/Activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        send_mail(mail_subject, message, 'noreply@karkhanay.com', [user.email],
                  fail_silently=False)

    def sendPasswordResetEmail(self, request, user):
        current_site = get_current_site(request)
        mail_subject = 'Reset your password.'
        message = render_to_string('E_Commerce/Password_Reset_Email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': password_reset_token.make_token(user),
        })
        send_mail(mail_subject, message, 'noreply@karkhanay.com', [user.email],
                  fail_silently=False)
