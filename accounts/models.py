from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import phone_validator


class User(AbstractUser):
    class Gender(models.TextChoices):
        MALE = 'M', 'Male'
        FEMALE = 'F', 'Female'
        UNSET = 'MF', 'Unset'

    phone = models.CharField(max_length=15, validators=[phone_validator], blank=True)
    address = models.TextField(blank=True)
    gender = models.CharField(max_length=2, choices=Gender.choices, default=Gender.UNSET)
    age = models.PositiveSmallIntegerField(blank=True, null=True)
    description = models.TextField(blank=True)

    @property
    def is_benefactor(self):
        return hasattr(self, 'benefactor')

    @property
    def is_charity(self):
        return hasattr(self, 'charity')
    

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     bio = models.TextField(null=True, blank=True)
#     nickname = models.CharField(blank=True, null=True, max_length=50)
#     location = models.CharField(blank=True, null=True, max_length=50)
#     avatar = models.ImageField(null=True)
#     weight = models.DecimalField(null=True, max_digits=5, decimal_places=2)
#     website = models.URLField(null=True, blank=True)
