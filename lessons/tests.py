from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import logout
from .models import BaseUser, Classroom, Lesson
from users.models import TeacherProfile


class BaseTest(TestCase):
    def setUp(self):
        self.login_url = reverse('index')
        self.home_url = reverse('home')
        self.notifications_url = reverse('my-notifications')
        self.classrooms_url = reverse('show-classrooms')
        self.join_classroom_url = reverse('join_classroom')

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

    def set_up_lesson(self, classroom):
        lesson = Lesson.objects.create(date=None,
                                       hour=None,
                                       subject='Temat lekcji',
                                       description='Opis lekcji',
                                       note='Notatka',
                                       owner=classroom.owner,
                                       classroom=classroom,
                                       lesson_done=False)
        lesson.save()
        return lesson

    def add_student_to_class(self):
        teacher = self.set_up_teacher()
        classroom = self.set_up_classroom(teacher)
        self.client.logout()

        user = self.set_up_user()
        self.client.post(self.classrooms_url, {'classroom_id':'abc123'}, format='text/html', secure=True)
        self.client.logout()

        self.client.post(self.login_url, {'email':'test@example.com',
                                                'password':'1234'}, format='text/html', secure=True)
        self.client.get(reverse('accept_join_classroom', args=[1]), secure=True)
        self.client.logout()

        self.client.post(self.login_url, {'email':'test@test.com',
                                                'password':'1234'}, format='text/html', secure=True)

        return user, classroom

    def add_student_to_class_with_lesson(self):
        teacher = self.set_up_teacher()
        classroom = self.set_up_classroom(teacher)
        lesson = self.set_up_lesson(classroom)
        self.client.logout()

        user = self.set_up_user()
        self.client.post(self.classrooms_url, {'classroom_id':'abc123'}, format='text/html', secure=True)
        self.client.logout()

        self.client.post(self.login_url, {'email':'test@example.com',
                                                'password':'1234'}, format='text/html', secure=True)
        self.client.get(reverse('accept_join_classroom', args=[1]), secure=True)
        self.client.logout()

        self.client.post(self.login_url, {'email':'test@test.com',
                                                'password':'1234'}, format='text/html', secure=True)

        return user, classroom, lesson


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

    def test_view_classroom_teacher(self):
        user = self.set_up_teacher()
        classroom = self.set_up_classroom(user)
        response = self.client.get(reverse('display-classroom', args=[classroom.id]), secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'display_classroom.html')
        self.client.logout()

    def test_view_classroom_student(self):
        user, classroom = self.add_student_to_class()
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

    def test_view_lesson_teacher(self):
        user = self.set_up_teacher()
        classroom = self.set_up_classroom(user)
        lesson = self.set_up_lesson(classroom)
        response = self.client.get(reverse('display-lesson', args=[classroom.id, lesson.id]), secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'display_lesson.html')
        self.client.logout()

    def test_view_lesson_student(self):
        user, classroom, lesson = self.add_student_to_class_with_lesson()
        response = self.client.get(reverse('display-lesson', args=[classroom.id, lesson.id]), secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'display_lesson.html')
        self.client.logout()

    # create classroom tests
    def test_create_classroom(self):
        user = self.set_up_teacher()
        response = self.client.post(self.classrooms_url, {'class_name':'Matematyka gr. 1',
                                                                'subject':'matematyka',
                                                                'owner': user}, format='text/html', secure=True)
        self.assertEqual(response.status_code, 302)
        self.client.logout()

    def test_create_classroom_full_data(self):
        user = self.set_up_teacher()
        response = self.client.post(self.classrooms_url, {'class_name':'Matematyka gr. 1',
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
        response = self.client.post(self.classrooms_url, {'classroom_id':'abc123'}, format='text/html', secure=True)
        self.assertEqual(response.status_code, 200) # to check (302?)
        self.client.logout()

    # student requests handling
    def test_accept_student_request(self):
        teacher = self.set_up_teacher()
        classroom = self.set_up_classroom(teacher)
        lesson = self.set_up_lesson(classroom)
        self.client.logout()

        user = self.set_up_user()
        self.client.post(self.classrooms_url, {'classroom_id':'abc123'}, format='text/html', secure=True)
        self.client.logout()

        self.client.post(self.login_url, {'email':'test@example.com',
                                                'password':'1234'}, format='text/html', secure=True)
        response = self.client.get(reverse('accept_join_classroom', args=[1]), secure=True)
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_reject_student_request(self):
        teacher = self.set_up_teacher()
        classroom = self.set_up_classroom(teacher)
        lesson = self.set_up_lesson(classroom)
        self.client.logout()

        user = self.set_up_user()
        self.client.post(self.classrooms_url, {'classroom_id':'abc123'}, format='text/html', secure=True)
        self.client.logout()

        self.client.post(self.login_url, {'email':'test@example.com',
                                                'password':'1234'}, format='text/html', secure=True)
        response = self.client.get(reverse('reject_join_classroom', args=[1]), secure=True)
        self.assertEqual(response.status_code, 200)
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

    # delete classroom tests
    def test_delete_classroom_teacher(self):
        user = self.set_up_teacher()
        classroom = self.set_up_classroom(user)
        response = self.client.get(reverse('delete-classroom', args=[classroom.id]), secure=True)
        self.assertEqual(response.status_code, 302)
        self.client.logout()

    # add lesson tests
    def test_add_lesson(self):
        user = self.set_up_teacher()
        classroom = self.set_up_classroom(user)
        response = self.client.post(reverse('display-classroom', args=[classroom.id]), {'subject':'Temat lekcji',
                                                                                        'description':'Opis lekcji',
                                                                                        'note':'Notatka',
                                                                                        'owner':user,
                                                                                        'classroom':classroom.id,
                                                                                        'lesson_done':False}, format='text/html', secure=True)
        self.assertEqual(response.status_code, 200) #302???
        self.client.logout()

    # modify lesson tests
    def test_modify_lesson_teacher(self):
        teacher = self.set_up_teacher()
        classroom = self.set_up_classroom(teacher)
        lesson = self.set_up_lesson(classroom)
        response = self.client.post(reverse('display-lesson', args=[classroom.id, lesson.id]), {'subject':'Temat lekcji 123',
                                                                                        'description':'Opis lekcji',
                                                                                        'note':'Notatka',
                                                                                        'date': '2021-12-01',
                                                                                        'hour': '01:10'}, format='text/html', secure=True)
        self.assertEqual(response.status_code, 302)
        self.client.logout()

    # delete lesson tests
    def test_delete_lesson(self):
        teacher = self.set_up_teacher()
        classroom = self.set_up_classroom(teacher)
        lesson = self.set_up_lesson(classroom)
        response = self.client.get(reverse('delete-lesson', args=[classroom.id, lesson.id]), secure=True)
        self.assertEqual(response.status_code, 302)
        self.client.logout()
