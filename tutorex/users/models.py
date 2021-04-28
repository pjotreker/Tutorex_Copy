from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from .managers import UserManager

# Create your models here.


class BaseUser(AbstractUser):
    username = None
    email = models.EmailField('email address', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    birthday = models.DateField()
    is_adult = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    phone_number = PhoneNumberField(null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"

