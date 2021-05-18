from django.db import models
from users.models import BaseUser, TeacherProfile
from django.core.validators import MinValueValidator, MaxValueValidator


class Lesson(models.Model):
    pass


class Classroom(models.Model):
    classroom_id = models.CharField(unique=True)
    subject = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255, unique=True)
    owner = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE)
    age_range_min = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(99)], blank=True)
    age_range_max = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(99)], blank=True)
    time_frame_start = models.DateField(blank=True)
    time_frame_end = models.DateField(blank=True)
    lessons = models.ManyToManyField(Lesson)
    students = models.ManyToManyField(BaseUser)

