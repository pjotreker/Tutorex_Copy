import pytest
from django.contrib.auth import authenticate, login, logout
from .models import BaseUser

@pytest.mark.django_db
def registration_test():
    new_user = BaseUser.objects.create_user(email='abc@abc.pl',
                                            password='1234',
                                            first_name='Koń',
                                            birthday=birthday,
                                            last_name='Rafał',
                                            is_active=False,
                                            is_teacher=False)
    assert BaseUser.objects.count() == 1
