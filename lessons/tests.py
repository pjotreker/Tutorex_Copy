from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import logout
from .models import BaseUser, Classroom
from users.models import TeacherProfile


class BaseTest(TestCase):
    def setUp(self):
        self.login_url = reverse('index')
        self.home_url = reverse('home')
        self.notifications_url = reverse('my-notifications')
        self.classrooms_url = reverse('show-classrooms')
        self.create_classroom_url = reverse('create-classroom')
        self.join_classroom_url = reverse('join-classroom')

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

    def set_up_classroom(self, teacher):
        tutor = TeacherProfile.objects.get(user=teacher)
        classroom = Classroom.objects.create(classroom_id='abc123',
                                             name='class_name',
                                             subject='subject',
                                             owner=tutor,
                                             age_range_min=0,
                                             age_range_max=99,
                                             time_frame_start='2021-05-23',
                                             time_frame_end='2022-05-23')

        classroom.save()
        return classroom


class NotificationTest(BaseTest):
    # view tests
    def test_view_home(self):
        user = self.set_up_user()
        response = self.client.get(self.home_url, secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main.html')

    def test_view_notifications(self):
        user = self.set_up_user()
        response = self.client.get(self.notifications_url, secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notifications_view.html')

    # notifications tests
    '''
    def test_view_profile(self):
        user = self.set_up_user()
        user_id = user.id
        response = self.client.get(reverse('user-edit-data', args=[user_id]), secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account.html')
    '''


class ClassroomTest(BaseTest):
    # view tests
    def test_view_classrooms_teacher(self):
        user = self.set_up_teacher()
        response = self.client.get(self.classrooms_url, secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_classrooms.html')
        self.client.logout()

    def test_view_classrooms_student(self):
        user = self.set_up_user()
        response = self.client.get(self.classrooms_url, secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_classrooms.html')
        self.client.logout()

    def test_view_create_classroom(self):
        user = self.set_up_teacher()
        response = self.client.get(self.create_classroom_url, secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_classroom.html')
        self.client.logout()

    def test_view_create_classroom_student(self):
        user = self.set_up_user()
        response = self.client.get(self.create_classroom_url, secure=True)
        self.assertEqual(response.status_code, 403)
        # self.assertTemplateUsed(response, 'create_classroom.html')
        self.client.logout()

    def test_view_join_classroom(self):
        user = self.set_up_user()
        response = self.client.get(self.join_classroom_url, secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'join_classroom.html')
        self.client.logout()

    def test_view_join_classroom_teacher(self):
        user = self.set_up_teacher()
        response = self.client.get(self.join_classroom_url, secure=True)
        self.assertEqual(response.status_code, 403)
        # self.assertTemplateUsed(response, 'join_classroom.html')
        self.client.logout()

    def test_view_classroom_teacher(self):
        user = self.set_up_teacher()
        classroom = self.set_up_classroom(user)
        response = self.client.get(reverse('display-classroom', args=[classroom.id]), secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'display_classroom.html')
        self.client.logout()

    def test_view_modify_classroom_teacher(self):
        user = self.set_up_teacher()
        classroom = self.set_up_classroom(user)
        response = self.client.get(reverse('modify-classroom', args=[classroom.id]), secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'modify_classroom.html')
        self.client.logout()

    '''
    def test_view_modify_classroom_student(self):
        teacher = self.set_up_teacher()
        classroom = self.set_up_classroom(teacher)
        class_id = classroom.id
        self.client.logout()

        user = self.set_up_user()
        response = self.client.get(reverse('modify-classroom', args=[class_id]), secure=True)
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, 'modify_classroom.html')
        self.client.logout()
    '''

    def test_view_delete_classroom_teacher(self):
        user = self.set_up_teacher()
        classroom = self.set_up_classroom(user)
        response = self.client.get(reverse('delete-classroom', args=[classroom.id]), secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'delete_classroom_ask.html')
        self.client.logout()

    # create classroom tests
    def test_create_classroom(self):
        user = self.set_up_teacher()
        response = self.client.post(self.create_classroom_url, {'class_name':'Matematyka gr. 1',
                                                                'subject':'matematyka',
                                                                'owner': user}, format='text/html', secure=True)
        self.assertEqual(response.status_code, 302)
        self.client.logout()

    def test_create_classroom_full_data(self):
        user = self.set_up_teacher()
        response = self.client.post(self.create_classroom_url, {'class_name':'Matematyka gr. 1',
                                                                'subject':'matematyka',
                                                                'owner': user,
                                                                'age_range_min':'0',
                                                                'age_range_max':'99',
                                                                'time_frame_start':'2021-05-23',
                                                                'time_frame_out':'2050-12-24'}, format='text/html', secure=True)
        self.assertEqual(response.status_code, 302)
        self.client.logout()

    # join classroom tests
    def test_join_classroom(self):
        teacher = self.set_up_teacher()
        classroom = self.set_up_classroom(teacher)
        self.client.logout()

        user = self.set_up_user()
        response = self.client.post(self.join_classroom_url, {'classroom_id':'abc123'}, format='text/html', secure=True)
        self.assertEqual(response.status_code, 200) # to check (302?)
        self.client.logout()

    # modify classroom tests
    def test_modify_classroom_teacher(self):
        user = self.set_up_teacher()
        classroom = self.set_up_classroom(user)
        response = self.client.post(reverse('modify-classroom', args=[classroom.id]),{'class_name':'Matematyka gr. 12',
                                                                'subject':'matematyka',
                                                                'owner': user,
                                                                'age_range_min':'0',
                                                                'age_range_max':'20',
                                                                'time_frame_start':'2021-05-23',
                                                                'time_frame_out':'2050-10-24'}, format='text/html', secure=True)
        self.assertEqual(response.status_code, 302)
        self.client.logout()
