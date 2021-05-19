from django.db import models
from users.models import BaseUser, TeacherProfile
from django.core.validators import MinValueValidator, MaxValueValidator


class Lesson(models.Model):
    pass


class Classroom(models.Model):
    classroom_id = models.CharField(max_length=40, unique=True)
    subject = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE)
    age_range_min = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(99)], null=True, blank=True, default=None)
    age_range_max = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(99)], null=True, blank=True, default=None)
    time_frame_start = models.DateField(blank=True, null=True, default=None)
    time_frame_end = models.DateField(blank=True, null=True, default=None)
    lessons = models.ManyToManyField(Lesson, default=None)
    students = models.ManyToManyField(BaseUser, default=None)

