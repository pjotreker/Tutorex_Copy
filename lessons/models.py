from django.db import models
from users.models import BaseUser, TeacherProfile
from django.core.validators import MinValueValidator, MaxValueValidator


class Lesson(models.Model):
    # data, godzina, temat, notatka, właściciel, zadanie domowe, pliki(?)
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
    lessons = models.ManyToManyField(Lesson)
    students = models.ManyToManyField(BaseUser)


class StudentClassRequest(models.Model):
    classroom_id = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    student_id = models.ForeignKey(BaseUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"Uczeń {self.student_id} chce dołączyć do klasy {self.classroom_id.name}"
