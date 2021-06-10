from django.conf import settings
from django.http import HttpResponseForbidden, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.safestring import mark_safe
from django.core.exceptions import PermissionDenied
from django.views.generic import TemplateView, View
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.template import loader
from django.urls import reverse
from notifications.signals import notify
import pdb

from users.models import TeacherProfile

from .models import Classroom, BaseUser, StudentClassRequest, Lesson, LessonTimeSlot
from .forms import CreateClassroomForm, ModifyClassroomForm, AddLessonForm, AddTimeSlotForm
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
        user_id = request.user
        student = BaseUser.objects.get(pk=user_id.id)
        try:
            classroom = Classroom.objects.get(classroom_id=classroom_id)
            join_classroom_request = StudentClassRequest.objects.create(
                classroom_id=classroom,
                student_id=student
            )
            teacher_user = classroom.owner.user
            notify.send(sender=user_id, recipient=teacher_user,
                        verb=f"Uczeń {user_id.first_name} {user_id.last_name} chce dołączyć do twojej klasy {classroom.name}",
                        request_id=join_classroom_request.id, need_acceptance=True)
            try:
                join_classroom_request.save()
            except:
                return HttpResponseForbidden("Nie udało się wysłać prośby o dołącznie do klasy, spróbuj ponownie")
        except (ValueError, TypeError, OverflowError, Classroom.DoesNotExist):
            return HttpResponseForbidden("Dana klasa nie istnieje!")

        return render(request, "request_sent.html")


class AcceptJoinClassroom(LoginRequiredMixin, View):
    def get(self, request, join_request_id):
        tmp_join_request = StudentClassRequest.objects.get(id=join_request_id)
        student_id = tmp_join_request.student_id
        classroom_id = tmp_join_request.classroom_id
        classroom_id.students.add(student_id)
        teacher = request.user
        classroom_id.save()
        tmp_join_request.delete()
        src_notification = teacher.notifications.filter(data__contains=join_request_id)
        if src_notification:
            src_notification[0].data['need_acceptance'] = False
            src_notification[0].save()
        notify.send(sender=teacher, recipient=student_id,
                    verb=mark_safe(f"{teacher.first_name} {teacher.last_name} dodał Cię do klasy <em> {classroom_id.name} </em>"),)
        return JsonResponse({'success': True})


class RejectJoinClassroom(LoginRequiredMixin, View):
    def get(self, request, join_request_id):
        tmp_join_request = StudentClassRequest.objects.get(id=join_request_id)
        tmp_join_request.delete()
        src_notification = request.user.notifications.filter(data__contains=join_request_id)
        if src_notification:
            src_notification[0].data['need_acceptance'] = False
            src_notification[0].save()
        return JsonResponse({'success': True})


class ModifyClassroom(LoginRequiredMixin, View):
    def get(self, request, class_id):
        owner = TeacherProfile.objects.get(user=request.user)
        classroom = Classroom.objects.get(id=class_id)
        if classroom.owner != owner:
            return HttpResponseForbidden("Nie możesz modyfikować nieswojej klasy!")
        if not request.user.is_teacher:
            return HttpResponseForbidden("Musisz byc nauczycielem aby modyfikować klasę!")
        return render(request, "modify_classroom.html", {'classroom': classroom})

    def post(self, request, class_id):
        owner = TeacherProfile.objects.get(user=request.user)
        classroom = Classroom.objects.get(id=class_id)
        if classroom.owner != owner:
            return HttpResponseForbidden("Nie możesz modyfikować nieswojej klasy!")
        if not request.user.is_teacher:
            return HttpResponseForbidden("Musisz byc nauczycielem aby modyfikować klasę!")
        form = ModifyClassroomForm(request.POST)
        try:
            if form.is_valid():
                class_name = form.cleaned_data.get('class_name')
                subject = form.cleaned_data.get('subject')
                age_range_min = form.cleaned_data.get('age_range_min')
                age_range_max = form.cleaned_data.get('age_range_max')
                time_frame_start = form.cleaned_data.get('time_frame_start')
                time_frame_end = form.cleaned_data.get('time_frame_end')
                if time_frame_start is None:
                    time_frame_start = classroom.time_frame_start
                if time_frame_end is None:
                    time_frame_end = classroom.time_frame_end
                classroom.name = class_name
                classroom.subject = subject
                classroom.age_range_min = age_range_min
                classroom.age_range_max = age_range_max
                classroom.time_frame_start = time_frame_start
                classroom.time_frame_end = time_frame_end

                classroom.save()
        except:
            return HttpResponseForbidden("Coś poszło nie tak :/ ")
        return redirect('show-classrooms')


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
            return render(request, "show_classrooms.html", {'classrooms_obj': classrooms })
            #return render(request, "show_classrooms.html", {'classrooms_obj': classrooms, 'students':students })

    def post(self, request):
        if request.user.is_teacher:
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
            return render(request, "show_classrooms.html", context) # empty display!
        if not request.user.is_teacher:
            classroom_id = request.POST.get('classroom_id')
            user_id = request.user
            student = BaseUser.objects.get(pk=user_id.id)
            try:
                classroom = Classroom.objects.get(classroom_id=classroom_id)
                join_classroom_request = StudentClassRequest.objects.create(
                    classroom_id=classroom,
                    student_id=student
                )
                teacher_user = classroom.owner.user
                notify.send(sender=user_id, recipient=teacher_user,
                            verb=f"Uczeń {user_id.first_name} {user_id.last_name} chce dołączyć do twojej klasy {classroom.name}",
                            request_id=join_classroom_request.id, need_acceptance=True)
                try:
                    join_classroom_request.save()
                except:
                    return HttpResponseForbidden("Nie udało się wysłać prośby o dołącznie do klasy, spróbuj ponownie")
            except (ValueError, TypeError, OverflowError, Classroom.DoesNotExist):
                return HttpResponseForbidden("Dana klasa nie istnieje!")

            return render(request, "request_sent.html")


class DisplayClassroom(LoginRequiredMixin, View):
    def get(self, request, classroom_id):
        classroom = Classroom.objects.get(id=classroom_id)
        if Lesson.objects.all().exists():
            lessons = Lesson.objects.filter(classroom=classroom)
        else:
            lessons = []
        students = classroom.students.all()
        return render(request, "display_classroom.html", {'classroom': classroom, 'students': students, 'lessons': lessons})

    def post(self, request, classroom_id):
        owner = TeacherProfile.objects.get(user=request.user)
        classroom = Classroom.objects.get(id=classroom_id)
        if classroom.owner != owner:
            return HttpResponseForbidden("Nie możesz modyfikować nieswojej klasy!")
        if not request.user.is_teacher:
            return HttpResponseForbidden("Musisz byc nauczycielem aby modyfikować klasę!")
        form = ModifyClassroomForm(request.POST)
        try:
            if form.is_valid():
                class_name = form.cleaned_data.get('class_name')
                subject = form.cleaned_data.get('subject')
                age_range_min = form.cleaned_data.get('age_range_min')
                age_range_max = form.cleaned_data.get('age_range_max')
                time_frame_start = form.cleaned_data.get('time_frame_start')
                time_frame_end = form.cleaned_data.get('time_frame_end')
                if time_frame_start is None:
                    time_frame_start = classroom.time_frame_start
                if time_frame_end is None:
                    time_frame_end = classroom.time_frame_end
                classroom.name = class_name
                classroom.subject = subject
                classroom.age_range_min = age_range_min
                classroom.age_range_max = age_range_max
                classroom.time_frame_start = time_frame_start
                classroom.time_frame_end = time_frame_end

                classroom.save()
        except:
            return HttpResponseForbidden("Coś poszło nie tak :/ ")
        students = []
        if Lesson.objects.all().exists():
            lessons = Lesson.objects.filter(classroom=classroom)
            for a in classroom.students.all():
                students.append(a.first_name + ' ' + a.last_name)
        else:
            for a in classroom.students.all():
                students.append(a.first_name + ' ' + a.last_name)
            lessons = []
        return render(request, "display_classroom.html", {'classroom': classroom, 'students': students, 'lessons': lessons})


class RemoveStudent(LoginRequiredMixin, View):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_teacher


    def post(self, request, classroom_id, student_id):
        resp = dict()
        try:
            student = BaseUser.objects.get(pk=student_id)
            classroom = Classroom.objects.get(pk=classroom_id)
            classroom.students.remove(student)
            classroom.save()
        except:
            resp = {'mssg': f'Nie udało usunąć sie ucznia {student.first_name} {student.last_name} z klasy, możliwe że uczeń lub klasa przestały istnieć'}
            resp = JsonResponse(resp)
            resp.status_code = 500
            return resp

        resp['mssg'] = f'Uczeń {student.first_name} {student.last_name} został usunięty z klasy'
        resp = JsonResponse(resp)
        resp.status_code = 200
        return resp


class DeleteClassroom(LoginRequiredMixin, View):
    def get(self, request, class_id):
        owner = TeacherProfile.objects.get(user=request.user)
        classroom = Classroom.objects.get(id=class_id)
        if classroom.owner != owner:
            return HttpResponseForbidden("Nie możesz usunąć nieswojej klasy!")
        if not request.user.is_teacher:
            return HttpResponseForbidden("Musisz byc nauczycielem aby móc usunąć klasę!")
        try:
            classroom.delete()
            return redirect('show-classrooms')
        except Exception:
            return HttpResponseForbidden("Coś poszło nieteges")


class AddLesson(LoginRequiredMixin, View):
    def get(self, request, classroom_id):

        try:
            owner = TeacherProfile.objects.get(user=request.user)
        except TeacherProfile.DoesNotExist:
            raise PermissionDenied("Musisz byc nauczycielem aby dodać lekcję!")
        classroom = Classroom.objects.get(id=classroom_id)
        if classroom.owner != owner:
            raise PermissionDenied("Nie możesz dodawać lekcji w nieswojej klasie!")
        return render(request, "add_lesson.html")

    def post(self, request, classroom_id):
        context = {}
        owner = TeacherProfile.objects.get(user=request.user)
        classroom = Classroom.objects.get(id=classroom_id)
        if classroom.owner != owner:
            return HttpResponseForbidden("Nie możesz dodawać lekcji w nieswojej klasie!")
        if not request.user.is_teacher:
            return HttpResponseForbidden("Musisz byc nauczycielem aby dodać lekcję!")
        form = AddLessonForm(request.POST)
        try:
            if form.is_valid():
                subject = form.cleaned_data.get('lesson_name')
                description = form.cleaned_data.get('description')
                note = form.cleaned_data.get('note')
                lesson_date = form.data.get('lesson_date')
                if lesson_date == '':
                    lesson_date = None
                lesson_hour = form.data.get('lesson_hour')
                if lesson_hour == '':
                    lesson_hour = None
                lesson_done = form.cleaned_data.get('lesson_done')
                try:
                    lesson = Lesson.objects.create(date=lesson_date,
                                                   hour=lesson_hour,
                                                   subject=subject,
                                                   description=description,
                                                   note=note,
                                                   owner=owner,
                                                   classroom=classroom,
                                                   lesson_done=lesson_done)
                except Exception:
                    return HttpResponseForbidden("Can't create the lesson")
                try:
                    lesson.save()
                except Exception:
                    return HttpResponseForbidden("Can't save the lesson")
            else:
                context['error'] = "Coś źle uzupełnione :( "
                return render(request, "display_lesson.html", context)
        except Exception:
            context['error'] = "Coś poszło nie tak"
            return render(request, "add_lesson.html", context)
        return redirect('display-classroom', classroom_id=classroom_id)


def redirectLessonData(request):
    date=request.POST['lesson_date'],
    hour=request.POST['lesson_hour'],
    subject=request.POST['lesson_name'],
    description=request.POST['description'],
    note=request.POST['note'],
    classroom=request.POST['classroom'],
    return redirect(AddLesson.post(request, classroom), {'lesson_name': subject,
                                                            'lesson_date': date,
                                                            'lesson_hour': hour,
                                                            'description': description,
                                                            'note': note})


class DisplayLesson(LoginRequiredMixin, View):
    def get(self, request, classroom_id, lesson_id):
        user_id = request.user.id
        user = BaseUser.objects.get(pk=user_id)
        classroom = Classroom.objects.get(id=classroom_id)
        lesson = Lesson.objects.get(pk=lesson_id)
        if user.is_teacher:
            owner = TeacherProfile.objects.get(user=request.user)
            if classroom.owner != owner or lesson.owner != owner:
                raise PermissionDenied("Nie powinno Cię tu być")
        else:
            students = classroom.students.all()
            print(students)
            print(user)
            if user not in students:
                raise PermissionDenied("Nie powinno Cię tu być uczniu")
        return render(request, "display_lesson.html", {'user': user, 'classroom': classroom, 'lesson': lesson})

    def post(self, request, classroom_id, lesson_id):
        subject = request.POST.get('subject', '').strip()
        description = request.POST.get('description', '').strip()
        note = request.POST.get('note', '').strip()
        date = request.POST.get('date', '')
        hour = request.POST.get('hour', '')
        try:
            lesson = Lesson.objects.filter(pk=lesson_id)
            lesson.update(subject=subject, description=description, note=note, date=date, hour=hour)
            return redirect('display-lesson', classroom_id=classroom_id, lesson_id=lesson_id)
        except:
            raise ValueError("Nie udało się zapisać klasy")


class CreateTimeSlot(LoginRequiredMixin, UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_teacher

    def get(self, request):
        today = datetime.today()
        return render(request, "add_timeslot.html", {'today': today})

    def post(self, request):

        form = AddTimeSlotForm(request.POST)
        if form.is_valid():
            time_start_date = form.cleaned_data.get('time_start_date')
            time_start_time = form.cleaned_data.get('time_start_time')
            slot_duration = form.cleaned_data.get('duration')
            time_start = datetime.combine(time_start_date, time_start_time)
            new_slot = LessonTimeSlot.objects.create(
                time_start=time_start,
                duration=slot_duration
            )

            new_slot.save()
            return HttpResponseRedirect(reverse('show-classrooms'))

        form = AddTimeSlotForm()
        today = datetime.today()
        return render(request, "add_timeslot.html", {'today': today})
