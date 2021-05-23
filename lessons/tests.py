from django.test import TestCase
from django.urls import reverse
from .models import BaseUser

class BaseTest(TestCase):
    def setUp(self):
        self.login_url = reverse('index')
        self.home_url = reverse('home')
        self.notifications_url = reverse('my-notifications')

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


class NotificationTest(BaseTest):
    def set_up(self):
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

    '''
    def set_up2(self):
        user = BaseUser.objects.create_user(email='test@example.com',
                                                password='1234',
                                                first_name='Konik',
                                                birthday='1999-01-01',
                                                last_name='Rafał',
                                                is_active=False,
                                                is_teacher=False)
        user.is_active = True
        user.save()
        return user
    '''

    # view tests
    def test_view_home(self):
        user = self.set_up()
        response = self.client.get(self.home_url, secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main.html')

    def test_view_notifications(self):
        user = self.set_up()
        response = self.client.get(self.notifications_url, secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notifications_view.html')

    # notifications tests
    '''
    def test_view_profile(self):
        user = self.set_up()
        user_id = user.id
        response = self.client.get(reverse('user-edit-data', args=[user_id]), secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account.html')
    '''
