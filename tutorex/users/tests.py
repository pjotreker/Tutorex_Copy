from django.test import TestCase
from django.urls import reverse
from .models import BaseUser

class BaseTest(TestCase):
    def setUp(self):
        self.register_url = reverse('signup-view')
        self.register_url_teacher = reverse('signup-view-teacher')
        self.register_url_parent = reverse('signup-view-parent')
        self.register_url_type = reverse('signup-choice-view')

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


class RegisterTest(BaseTest):
    # view tests
    def test_view_page(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup_form.html')

    def test_view_page_teacher(self):
        response = self.client.get(self.register_url_teacher)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup_form_teacher.html')

    def test_view_page_parent(self):
        response = self.client.get(self.register_url_parent)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup_form_parent.html')

    def test_view_page_register_type(self):
        response = self.client.get(self.register_url_type)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register_type.html')

    # registration tests
    def test_register_user(self):
        response = self.client.post(self.register_url, self.user, format='text/html')
        self.assertEqual(response.status_code, 302)

    def test_register_teacher(self):
        response = self.client.post(self.register_url_teacher, self.user_teacher, format='text/html')
        self.assertEqual(response.status_code, 302)

    def test_register_parent(self):
        response = self.client.post(self.register_url_parent, self.user_parent, format='text/html')
        self.assertEqual(response.status_code, 302)

class LoginTest(BaseTest):
    # view tests
    def test_view_page(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    # login tests
    def test_login_success(self):
        user = BaseUser.objects.create_user(email='test@test.com',
                                                password='1234',
                                                first_name='Koń',
                                                birthday='1999-01-01',
                                                last_name='Rafał',
                                                is_active=False,
                                                is_teacher=False)
        user.is_active = True
        user.save()
        response = self.client.post(self.login_url, {'email':'test@test.com',
                                                'password':'1234'}, format='text/html')
        self.assertEqual(response.status_code, 302)

    def test_login_unactive(self):
        user = BaseUser.objects.create_user(email='test@test.com',
                                                password='1234',
                                                first_name='Koń',
                                                birthday='1999-01-01',
                                                last_name='Rafał',
                                                is_active=False,
                                                is_teacher=False)
        user.save()
        response = self.client.post(self.login_url, {'email':'test@test.com',
                                                'password':'1234'}, format='text/html')
        self.assertEqual(response.status_code, 200) # should there be different status_code?
