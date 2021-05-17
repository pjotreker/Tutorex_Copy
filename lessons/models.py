from django.db import models
from users.models import BaseUser, TeacherProfile
from django.core.validators import MinValueValidator, MaxValueValidator


class Lesson(models.Model):
    pass


class Classroom(models.Model):
    classroom_id = models.CharField(primary_key=True)
    subject = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255, unique=True)
    owner = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE)
    age_range = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(99)], blank=True)
    time_frame = models.CharField(max_length=255)
    lessons = models.ManyToManyField(Lesson)
    students = models.ManyToManyField(BaseUser)

