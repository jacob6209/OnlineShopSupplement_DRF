"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from datetime import timedelta
import os
from pathlib import Path
from environs import Env

# from core.models import CustomUser


# for environments variables
env = Env()
env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
BASE_URL = 'http://192.168.52.57:8000'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-r8xs3@%bid*q6(5$xo%f=0##n+w!vvqqb(r!z_ei9cecntez^m'
SECRET_KEY = env("DJANGO_SECRET_KEY")

# For Twilio Setting:-------------------------------
TWILIO_ACCOUNT_SID =env("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = env("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = env("TWILIO_PHONE_NUMBER")
#----------------------------------------------------

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DJANGO_DEBUG")

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '192.168.52.57','192.168.204.57','192.168.0.102','192.168.12.57','192.168.188.57']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'rest_framework',
    'rest_framework_simplejwt',
    'djoser',
    'debug_toolbar',
    'store',
    'core',
    'account',
    'orders',
    'payment',
    
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

INTERNAL_IPS = [
    "127.0.0.1",
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'store2',
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': 'mysql',
         'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# settings.py

# Static files (CSS, JavaScript, images)
#static File config
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]  # Path to your static files directory

#media File
MEDIA_URL='/media/'
MEDIA_ROOT=str(BASE_DIR.joinpath('media'))
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK={

    "COERCE_DECIMAL_TO_STRING": False,
    # 'PAGE_SIZE':10,
   'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        
    )
}
SIMPLE_JWT={
    # 'AUTH_HEADER_TYPES':(),
    'AUTH_HEADER_TYPES':('JWT'),
    'ACCESS_TOKEN_LIFETIME': timedelta(days=30),  # Access token expires in 30 days
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),  # Refresh token also expires in 30 days

}

AUTH_USER_MODEL='core.CustomUser'

DJOSER={

    'LOGIN_FIELD': 'email',
    'USERNAME_FIELD':'email',
    "USER_ID_FIELD": 'email',
    "SEND_ACTIVATION_EMAIL": True,
    "ACTIVATION_URL": "activate/{uid}/{token}",

    # 'ACTIVATION_VIEW': 'core.views.custom_activation_view',

    "PASSWORD_RESET_CONFIRM_URL": "password/reset/confirm/{uid}/{token}",  # the reset link
    'USERNAME_RESET_CONFIRM_URL': "email/reset/confirm/{uid}/{token}",
    # 'USER_CREATE_PASSWORD_RETYPE':True,
    'USERNAME_CHANGED_EMAIL_CONFIRMATION':True,
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION':True,
    'SEND_CONFIRMATION_EMAIL':False,
    # 'SET_USERNAME_RETYPE':True,
    # 'SET_PASSWORD_RETYPE':True,

    'SERIALIZERS':{
    # 'user_create': 'account.serializers.UserCreateSerializer',
    # 'current_user': 'account.serializers.UserSerializer',
    # # 'user': 'account.serializers.UserCreateSerializer',
    # 'user_delete': 'djoser.serializers.UserDeleteSerializer',
        # hajizadeh whay
        'user_create':'core.serializers.UserCreateSerializer',
        'current_user':'core.serializers.UserSerializer',
        # my Soulotion
                # "user_create": "accounts.tokens.AccountActivationTokenGenerator",
                # "user": "accounts.tokens.AccountActivationTokenGenerator",

    },
    
    'EMAIL': {
        'activation': 'account.email.ActivationEmail',
        'confirmation': 'account.email.ConfirmationEmail',
        'password_reset': 'account.email.PasswordResetEmail',
        'password_changed_confirmation': 'account.email.PasswordChangedConfirmationEmail',
    },
}



# ---------------  Mail Service  Setting  ------------------#
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
SITE_NAME = "Jac Supplemnts"
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = env("DJANGO_EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("DJANGO_EMAIL_HOST_PASSWORD")







