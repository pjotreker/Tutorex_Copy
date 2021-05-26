from tkinter import Entry

from django.conf import settings
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import TemplateView, View
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template import loader
from notifications.signals import notify

from users.models import TeacherProfile

from .models import Classroom, BaseUser, StudentClassRequest
from .forms import CreateClassroomForm
from datetime import datetime
import re

# Create your views here.


def create_code():
    now = datetime.utcnow()
    dt_string = now.strftime('%Y%m%d%H%M%S%f')  # day-month-year-hour-min-sec-milisec
    string = re.sub('1', 'X', dt_string)
    string_2 = re.sub('2', 'Z', string)
    code = re.sub('6', 'Z', string_2)
    return code


class CreateClassroom(LoginRequiredMixin, View):
    def get(self, request):
        if not request.user.is_teacher:
            return HttpResponseForbidden("Musisz być nauczycielem żeby moc dodac klasę!")
        return render(request, "create_classroom.html")

    def post(self, request):
        context = {}
        form = CreateClassroomForm(request.POST)
        classroom_id = create_code()
        if form.is_valid():
            class_name = form.cleaned_data.get('class_name')
            subject = form.cleaned_data.get('subject')
            owner = TeacherProfile.objects.get(user=request.user)
            age_range_min = form.cleaned_data.get('age_range_min')
            age_range_max = form.cleaned_data.get('age_range_max')
            time_frame_start = form.cleaned_data.get('time_frame_start')
            time_frame_end = form.cleaned_data.get('time_frame_end')

            classroom = Classroom.objects.create(classroom_id=classroom_id,
                                                 name=class_name,
                                                 subject=subject,
                                                 owner=owner,
                                                 age_range_min=age_range_min,
                                                 age_range_max=age_range_max,
                                                 time_frame_start=time_frame_start,
                                                 time_frame_end=time_frame_end)
            try:
                classroom.save()
            except:
                raise ValueError("Nie udało się utworzyc klasy :C")
            return redirect('classroom-created-success', classroom_id=classroom_id)
        context['error'] = "Ajjj coś poszło nie tak"
        return render(request, "create_classroom.html", context)


class ClassroomCreated(LoginRequiredMixin, View):
    def get(self, request, classroom_id):
        context = {'classroom_id': classroom_id}
        return render(request, "classroom_created_success.html", context)


class JoinClassroom(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_teacher:
            return HttpResponseForbidden("Musisz byc uczniem zeby dolaczyc do klasy!")
        return render(request, "join_classroom.html")

    def post(self, request):
        classroom_id = request.POST.get('classroom_id')
        user_id = request.user.id
        student = BaseUser.objects.get(pk=user_id)
        try:
            classroom = Classroom.objects.get(classroom_id=classroom_id)
            join_classroom_request = StudentClassRequest.objects.create(
                classroom_id=classroom,
                student_id=student
            )
            try:
                join_classroom_request.save()
            except:
                return HttpResponseForbidden("Nie udało się wysłać prośby o dołącznie do klasy, spróbuj ponownie")
        except (ValueError, TypeError, OverflowError, Classroom.DoesNotExist):
            return HttpResponseForbidden("Dana klasa nie istnieje!")

        return render(request, "request_sent.html")


# to jeszcze nie było odpalane także do sprawdzenia pracuję nad tym na innym branchu tosię tu przypadkowo znalazło xD
class ModifyClassroom(LoginRequiredMixin, View):
    def get(self, request, class_id):
        owner = TeacherProfile.objects.get(user=request.user)
        classroom = Classroom.objects.get(id=class_id)
        if classroom.owner != owner:
            return HttpResponseForbidden("Nie możesz modyfikować nieswojej klasy!")
        if not request.user.is_teacher:
            return HttpResponseForbidden("Musisz byc nauczycielem aby modyfikować klasę!")
        return render(request, "join_classroom.html")

    def post(self, request, class_id):
        owner = TeacherProfile.objects.get(user=request.user)
        classroom = Classroom.objects.get(id=class_id)
        if classroom.owner != owner:
            return HttpResponseForbidden("Nie możesz modyfikować nieswojej klasy!")
        if not request.user.is_teacher:
            return HttpResponseForbidden("Musisz byc nauczycielem aby modyfikować klasę!")
        form = CreateClassroomForm(request.POST)    # czy ten sam form może być?
        if form.is_valid():
            class_name = form.cleaned_data.get('class_name')
            subject = form.cleaned_data.get('subject')
            age_range_min = form.cleaned_data.get('age_range_min')
            age_range_max = form.cleaned_data.get('age_range_max')
            time_frame_start = form.cleaned_data.get('time_frame_start')
            time_frame_end = form.cleaned_data.get('time_frame_end')

            classroom.name = class_name
            classroom.subject = subject
            classroom.age_range_min = age_range_min
            classroom.age_range_max = age_range_max
            classroom.time_frame_start = time_frame_start
            classroom.time_frame_end = time_frame_end

            classroom.save()
        return redirect('display-classroom')


class ShowClassrooms(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_teacher:
            owner = TeacherProfile.objects.get(user=request.user)
            classrooms = Classroom.objects.filter(owner=owner)
            return render(request, "show_classrooms.html", {'classrooms_obj': classrooms})
        if not request.user.is_teacher:
            user = request.user
            user_id = user.id
            student = BaseUser.objects.get(pk=user_id)
            classrooms = Classroom.objects.filter(students=student)
            return render(request, "show_classrooms.html", {'classrooms_obj': classrooms})


class DisplayClassroom(LoginRequiredMixin, View):
    def get(self, request, classroom_id):
        classroom = Classroom.objects.get(id=classroom_id)
        return render(request, "display_classroom.html", {'classroom': classroom})
