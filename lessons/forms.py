from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from .models import BaseUser, Classroom
from datetime import date


class CreateClassroomForm(forms.ModelForm):
    class_name = forms.CharField(max_length=255)
    subject = forms.CharField(max_length=255, required=False)
    age_range_min = forms.IntegerField(required=False, validators=[MinValueValidator(0), MaxValueValidator(99)])
    age_range_max = forms.IntegerField(required=False, validators=[MinValueValidator(0), MaxValueValidator(99)])
    time_frame_start = forms.DateField(required=False, widget=forms.DateInput())
    time_frame_end = forms.DateField(required=False, widget=forms.DateInput())

    class Meta:
        model = Classroom
        fields = ["class_name", "subject", "age_range_min", "age_range_max", "time_frame_start", "time_frame_end"]


class ModifyClassroomForm(forms.Form):
    class_name = forms.CharField(max_length=80)
    subject = forms.CharField(max_length=255, required=False)
    age_range_min = forms.IntegerField(required=False, validators=[MinValueValidator(0), MaxValueValidator(99)])
    age_range_max = forms.IntegerField(required=False, validators=[MinValueValidator(0), MaxValueValidator(99)])
    time_frame_start = forms.DateField(required=False, widget=forms.DateInput())
    time_frame_end = forms.DateField(required=False, widget=forms.DateInput())

    class Meta:
        model = Classroom
        fields = ["class_name", "subject", "age_range_min", "age_range_max", "time_frame_start", "time_frame_end"]
