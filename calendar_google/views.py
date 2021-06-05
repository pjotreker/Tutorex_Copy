from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden, JsonResponse
from .models import BaseUser
from django.core.exceptions import PermissionDenied


class ShowCalendarTeacher(LoginRequiredMixin, View):
        def get(self, request, user_uid):
            try:
                user = BaseUser.objects.get(pk=user_uid)
                if user.id != request.user.id or not request.user.id:
                    raise PermissionDenied
            except (ValueError, TypeError, OverflowError, BaseUser.DoesNotExist):
                user = None
            if user and request.user.is_teacher:
                context={'user_uid':user_uid}
                return render(request, "show_calendar_teacher.html", context)
            else:
                HttpResponseForbidden("Błąd z uwierzytelnieniem. Skontaktuj się z administratorami.")


class ShowCalendarStudent(LoginRequiredMixin, View):
    def get(self, request, user_uid):
        try:
            user = BaseUser.objects.get(pk=user_uid)
            if user.id != request.user.id or not request.user.id:
                raise PermissionDenied
        except (ValueError, TypeError, OverflowError, BaseUser.DoesNotExist):
            user = None
        if user and not request.user.is_teacher:
            context = {'user_uid': user_uid}
            return render(request, "show_calendar_student.html", context)
        else:
            HttpResponseForbidden("Błąd z uwierzytelnieniem. Skontaktuj się z administratorami.")


class ShowCalendar(LoginRequiredMixin, View):
    def get(self, request):
        try:
            user_id = request.user.id
            user = BaseUser.objects.get(pk=user_id)
        except (ValueError, TypeError, OverflowError, BaseUser.DoesNotExist):
            user = None
        if user.is_teacher:
            return render(request, "show_calendar_teacher.html")
        else:
            return render(request, "show_calendar_student.html")
