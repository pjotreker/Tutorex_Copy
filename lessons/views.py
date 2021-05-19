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

from .models import Classroom
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
        classroom_id = create_code()
        class_name = request.POST.get('class_name')
        subject = request.POST.get('subject')
        owner = request.user
        age_range_min = request.POST.get('age_range_min')
        age_range_max = request.POST.get('age_range_max')
        time_frame_start = request.POST.get('time_frame_start')
        time_frame_end = request.POST.get('time_frame_end')

        classroom = Classroom(classroom_id=classroom_id,
                              class_name=class_name,
                              subject=subject,
                              owner=owner,
                              age_range_min=age_range_min,
                              age_range_max=age_range_max,
                              time_frame_start=time_frame_start,
                              time_frame_end=time_frame_end)
        if classroom.save():
            return redirect('class-created-success', classroom_id=classroom_id)
        else:
            raise ValueError("Nie udało się utworzyc klasy :C")

        # return render(request, "create_classroom.html", context)


class ClassroomCreated(View):
    def get(self, request, classroom_id):
        context = {'classroom_id': classroom_id}
        return render(request, "classroom_created_success.html", context)
