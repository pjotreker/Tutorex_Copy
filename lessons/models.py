from django.db import models
from users.models import BaseUser, TeacherProfile
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime, timedelta
from django.core.files.storage import FileSystemStorage


class LessonMaterials(models.Model):
    # tu będzie musił być klucz obcy do lekcji (bo będzie wiele materiałów do 1 lekcji)
    pass


class Classroom(models.Model):
    classroom_id = models.CharField(max_length=40, unique=True)
    subject = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=80)
    owner = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE)
    age_range_min = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(99)], null=True, blank=True, default=None)
    age_range_max = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(99)], null=True, blank=True, default=None)
    time_frame_start = models.DateField(blank=True, null=True, default=None)
    time_frame_end = models.DateField(blank=True, null=True, default=None)
    students = models.ManyToManyField(BaseUser)


class Lesson(models.Model):
    date = models.DateField(blank=True, null=True)
    hour = models.TimeField(blank=True, null=True)
    subject = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True, null=True)
    note = models.CharField(max_length=1000, blank=True, null=True)
    owner = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, default=None)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, default=None)
    lesson_done = models.BooleanField(default=False)


class LessonTimeSlot(models.Model):
    lesson_id = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    time_start = models.DateTimeField()
    duration = models.IntegerField(default=45)
    students = models.ManyToManyField(BaseUser)

    def calculate_time_end(self):
        return self.time_start + timedelta(minutes=self.duration)


class StudentClassRequest(models.Model):
    classroom_id = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    student_id = models.ForeignKey(BaseUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"Uczeń {self.student_id} chce dołączyć do klasy {self.classroom_id.name}"
