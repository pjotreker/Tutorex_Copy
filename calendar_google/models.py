from django.db import models
from users.models import BaseUser, TeacherProfile
from django.core.validators import MinValueValidator, MaxValueValidator

class Calendar(models.Model):
    pass