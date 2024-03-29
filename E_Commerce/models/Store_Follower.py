from django.db import models
from django_extensions.db.models import TimeStampedModel
from E_Commerce.models import Customer, Store


class Store_Follower(TimeStampedModel):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
