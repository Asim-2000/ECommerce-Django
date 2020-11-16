from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django_extensions.db.models import TimeStampedModel


class Product_Category(TimeStampedModel):
    name = models.CharField(max_length=30, null=False)
    commission = models.FloatField(null=False, default=0.1, validators=[MaxValueValidator(100), MinValueValidator(0)])
    description = models.CharField(max_length=1000)
    category_image = models.ImageField()

    class Meta:
        verbose_name_plural = "Product Categories"

    def __str__(self):
        return self.name