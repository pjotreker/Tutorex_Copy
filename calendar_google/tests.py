from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import logout
from .models import BaseUser
from users.models import TeacherProfile


class BaseTest(TestCase):
    def setUp(self):
        self.login_url = reverse('index')

        self.user = {
            'email':'test@example.com',
            'password':'1234',
            'password2':'1234',
            'first_name':"Koń",
            'birthday':'1999-01-01',
            'last_name':"Rafał",
            'is_teacher':False
        }

        self.user_teacher = {
            'email':'tutor@example.com',
            'password':'1234',
            'password2':'1234',
            'first_name':"Pan",
            'birthday':'1986-10-12',
            'last_name':"Nauczyciel",
            'is_teacher':True
        }

        self.user_parent = {
            'email':'rodzic@example.com',
            'password':'1234',
            'password2':'1234',
            'parent_password':'9876',
            'parent_password2':'9876',
            'first_name':"Poważny",
            'birthday':'2005-04-01',
            'last_name':"Prawnik",
            'is_teacher':False
        }

        return super().setUp()

    def set_up_user(self):
        user = BaseUser.objects.create_user(email='test@test.com',
                                                password='1234',
                                                first_name='Koń',
                                                birthday='1999-01-01',
                                                last_name='Rafał',
                                                is_active=False,
                                                is_teacher=False)
        user.is_active = True
        user.save()
        self.client.post(self.login_url, {'email':'test@test.com',
                                                'password':'1234'}, format='text/html', secure=True)
        return user

    def set_up_teacher(self):
        user = BaseUser.objects.create_user(email='test@example.com',
                                                password='1234',
                                                first_name='Srogi',
                                                birthday='1999-01-01',
                                                last_name='Nauczyciel',
                                                is_active=False,
                                                is_teacher=True)
        user.is_active = True
        user.save()
        self.client.post(self.login_url, {'email':'test@example.com',
                                                'password':'1234'}, format='text/html', secure=True)
        return user


class CalendarTest(BaseTest):
    # view tests
    def test_view_month_student(self):
        user = self.set_up_user()
        user_id = user.id
        response = self.client.get(reverse('show-calendar-student', args=[user_id]), secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_calendar_student.html')

    def test_view_month_teacher(self):
        user = self.set_up_teacher()
        user_id = user.id
        response = self.client.get(reverse('show-calendar-teacher', args=[user_id]), secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_calendar_teacher.html')

    def test_view_week_student(self):
        user = self.set_up_user()
        user_id = user.id
        response = self.client.get(reverse('show-calendar-week-student', args=[user_id]), secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_calendar_week_student.html')

    def test_view_week_teacher(self):
        user = self.set_up_teacher()
        user_id = user.id
        response = self.client.get(reverse('show-calendar-week-teacher', args=[user_id]), secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_calendar_week_teacher.html')

    # 403 views
    def test_view_month_student_as_teacher(self):
        user = self.set_up_teacher()
        user_id = user.id
        response = self.client.get(reverse('show-calendar-student', args=[user_id]), secure=True)
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403_auth.html')

    def test_view_month_teacher_as_student(self):
        user = self.set_up_user()
        user_id = user.id
        response = self.client.get(reverse('show-calendar-teacher', args=[user_id]), secure=True)
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403_auth.html')

    def test_view_week_student_as_teacher(self):
        user = self.set_up_teacher()
        user_id = user.id
        response = self.client.get(reverse('show-calendar-week-student', args=[user_id]), secure=True)
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403_auth.html')

    def test_view_week_teacher_as_student(self):
        user = self.set_up_user()
        user_id = user.id
        response = self.client.get(reverse('show-calendar-week-teacher', args=[user_id]), secure=True)
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403_auth.html')
