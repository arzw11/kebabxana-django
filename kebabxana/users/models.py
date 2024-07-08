from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    phone_number = PhoneNumberField(region='RU', unique=True)
    date_birth = models.DateTimeField(blank=True, null=True, verbose_name='Дата рождения')