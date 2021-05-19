from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.dispatch import receiver
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

    phone_number = PhoneNumberField(blank=True, null=True, default=None)
    parent_password = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"


class TeacherProfile(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"Nauczyciel {self.user.first_name} {self.user.last_name} - {self.user.email}"


@receiver(post_save, sender=BaseUser)
def create_teacher_profile(sender, instance, created, **kwargs):
    if created and instance.is_teacher:
        TeacherProfile.objects.create(user=instance)


