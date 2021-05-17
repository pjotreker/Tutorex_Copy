import datetime

from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):

	def create_user(self, email, password, **user_fields):
		if not email:
			raise ValueError("Email is not set!")
		email = self.normalize_email(email)
		user = self.model(email=email, **user_fields)
		user.set_password(password)
		user.save()
		return user

	def create_superuser(self, email, password, **user_fields):
		user_fields.setdefault('is_staff', True)
		user_fields.setdefault('is_superuser', True)
		user_fields.setdefault('is_active', True)

		if user_fields.get('is_staff') is not True:
			raise ValueError('Superuser must have is_staff=True.')
		if user_fields.get('is_superuser') is not True:
			raise ValueError('Superuser must have is_superuser=True.')
		superuser_birthday = datetime.datetime(1970, 1, 1)
		if not user_fields.get('birthday'):
			user_fields['birthday'] = superuser_birthday
		return self.create_user(email, password, **user_fields)
