"""
Django settings for funticket project.

Generated by 'django-admin startproject' using Django 5.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
from pathlib import Path

from datetime import timedelta
from django.core.management.utils import get_random_secret_key

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
BASE_URL = os.environ.get('FT_BASE_URL', 'http://127.0.0.1:8000')

# https://docs.djangoproject.com/en/4.2/ref/settings/#site-id
SITE_ID = 1

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATICROOT = os.environ.get('STATIC_ROOT', os.path.join(BASE_DIR, 'static_files'))
STATIC_ROOT = STATICROOT
STATIC_URL = '/static/'

MEDIAROOT = os.environ.get('MEDIA_ROOT', os.path.join(BASE_DIR, 'media_files'))
MEDIA_ROOT = MEDIAROOT
MEDIA_URL = '%s/media_files/' % (BASE_URL)
MEDIA_RELATIVE_URL = '/media_files/'

# Datebase
DB_HOST = os.environ.get('FT_DB_HOST', 'localhost')
DB_PORT = int(os.environ.get('FT_DB_PORT', '5432'))
DB_NAME = os.environ.get('FT_DB_NAME', 'funticketdb')
DB_USER = os.environ.get('FT_DB_USER', 'postgres')
DB_PASSWORD = os.environ.get('FT_DB_PASSWORD')

# Redis
REDIS_HOST = os.environ.get('FT_REDIS_HOST', 'localhost')
REDIS_PORT = int(os.environ.get('FT_REDIS_PORT', '6379'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("FT_DSCY", get_random_secret_key())

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('FT_DEBUG', 'false').lower() == 'true'

# https://docs.djangoproject.com/en/4.2/ref/settings/#allowed-hosts
ALLOWED_HOSTS = os.environ.get('FT_DOMAINS', '*').strip('"').split(',')

# https://docs.djangoproject.com/en/4.2/ref/settings/#internal-ips
INTERNAL_IPS = ['127.0.0.1']

# Rest framework
REST_FRAMEWORK = {
    # Apis authentication_classes = This:
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

# JWT Config
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=6) if DEBUG is False else timedelta(hours=2),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=365 * 2) if DEBUG is False else timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
}

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    'debug_toolbar',
    'rest_framework_simplejwt',
    'import_export',
    'drf_yasg',
    'reversion',
    'leaflet',
    'media',
    'users',
    'geo',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',


]

ROOT_URLCONF = 'funticket.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'funticket.wsgi.application'

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
SESSION_COOKIE_HTTPONLY = True
# Session less
SESSION_COOKIE_SECURE = False
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
        'CONN_MAX_AGE': 150,
        'TEST': {
            'NAME': 'test_{}'.format(os.environ.get('FT_TEST_DB', DB_NAME)),
        }
    }
}

# User
AUTH_USER_MODEL = 'users.User'

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    },
    'USE_SESSION_AUTH': False

}

# Auth
# TODO: check changing order (for performance)
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'users.backends.UserBackend',
]

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

# SWAGGER CONFIG

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    },
    'USE_SESSION_AUTH': False
}

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'fa-ir'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L18N = True

USE_L10N = True

USE_TZ = True


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOCALE_PATHS = [
    os.path.join(BASE_DIR, "locale"),
]

# GDAL_LIBRARY_PATH = "/home/SAEED/lib/libgdal.so.31"

if DEBUG is False:
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = [
        'rest_framework.renderers.JSONRenderer',
    ]
    # https://docs.djangoproject.com/en/4.2/ref/settings/#std-setting-CSRF_COOKIE_SECURE
    CSRF_COOKIE_SECURE = True
    CSRF_TRUSTED_ORIGINS = os.environ.get('FT_TRUSTED_ORIGINS', "http://localhost").strip('"').split(' ')
    print(CSRF_TRUSTED_ORIGINS)

print(DEBUG)