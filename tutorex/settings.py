"""
Django settings for tutorex project.

Generated by 'django-admin startproject' using Django 3.0.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from django.conf.global_settings import DATABASES

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

##baza
import dj_database_url
DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'otbziimne0%k@nngq*1mb6ryz#5z=gb!50y$d$&ydn77zi)03t'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['tutorex-test.herokuapp.com', 'tutorex-app.herokuapp.com', '127.0.0.1', 'localhost', 'tutorex.azurewebsites.net', '*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'phonenumber_field',
    'lessons',
    'users',
    'notifications',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]



ROOT_URLCONF = 'tutorex.urls' ###
DJANGO_NOTIFICATIONS_CONFIG = {'USE_JSONFIELD': True}

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [(os.path.join(BASE_DIR, 'tutorex/templates'))],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'tutorex.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# DBHOST is only the server name, not the full URL
hostname = 'tutorexserver'

# Configure Postgres database; the full username is username@servername,
# which we construct using the DBHOST value.
import sys
# '''
if 'test' in sys.argv:
    DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.sqlite3',
             'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
         }
     }
else:
    DATABASES = {
        'default': {
         'ENGINE': 'django.db.backends.postgresql',
         'NAME': "d2hevt4sscj1g7",
         'HOST': "ec2-52-19-170-215.eu-west-1.compute.amazonaws.com",
         'USER': 'bfadhmhbmjxfmh',
         'PASSWORD': 'b0d452b1886cd23d29fb4341abc541929d8c5ee55b668c65d1daf9bc25567630',
         'PORT':'5432'
        }
    }
# '''
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
'''
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "tutorextest@gmail.com"
EMAIL_HOST_PASSWORD = "U&zra#!8Hy"
DEFAULT_FROM_MAIL = EMAIL_HOST_USER


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators
AUTH_USER_MODEL = "users.BaseUser"

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "tutorex/static")
STATIC_URL = '/static/'
LOGIN_URL = '/login/'

PHONENUMBER_DEFAULT_REGION = "PL"
