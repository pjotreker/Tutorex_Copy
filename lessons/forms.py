from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from .models import BaseUser, Classroom, Lesson, LessonTimeSlot
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

    # class Meta:
    #    model = Classroom
    #    fields = ["class_name", "subject", "age_range_min", "age_range_max", "time_frame_start", "time_frame_end"]


class AddLessonForm(forms.ModelForm):
    lesson_name = forms.CharField(max_length=100)
    description = forms.CharField(required=False, max_length=255)
    note = forms.CharField(required=False, max_length=1000)
    date = forms.DateField(required=False, widget=forms.DateInput())
    hour = forms.TimeField(required=False, input_formats=['%H:%M'], widget=forms.TimeInput())
    lesson_done = forms.BooleanField(required=False)

    class Meta:
        model = Lesson
        fields = ["lesson_name", "description", "note", "date", "hour", "lesson_done"]


class AddTimeSlotForm(forms.Form):
    time_start_date = forms.DateField()
    time_start_time = forms.TimeField(input_formats=['%H:%M'], widget=forms.TimeInput(attrs={'class':'timepicker'}))
    duration = forms.IntegerField(initial=45)

    # class Meta:
    #     model = LessonTimeSlot
    #     fields = ['duration']
