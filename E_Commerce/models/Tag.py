from django.db import models
from django_extensions.db.models import TimeStampedModel


class Tag(TimeStampedModel):
    name = models.CharField(max_length=30)
    slug = models.CharField(max_length=30)
    description = models.CharField(max_length=500)
