"""
Project name = website
Website name = Khan Diary
Website Domain = www.khandiary.com
dajngo version = 3.1.6.
"""

from pathlib import Path
from django.contrib.messages import constants as message_constants
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'obabp&*vk@s7!q&6t#onci(#hi32zmtdx8vc@)u)2)-bg$!4_+'

# Hosts Setting
ALLOWED_HOSTS = ["*"]

# Application Definition

INSTALLED_APPS = [
    # Website Apps
    'khandiary',  # Manages whole website ex- privacy, terms, contact us, index etc.
    'entries',  # Manages diary entry writing.
    'users.apps.UsersConfig',  # Manages profile & authentication stuff.
    'notifications',  # Manages notifications of site.

    'simple_pagination',

    'django_user_agents', # Used for checking device, browser used by user.

    # Default Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# Middlewares
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware', # User agent middleware
]

# Root URL Configuration
ROOT_URLCONF = 'website.urls' 
COUNTRIES_FLAG_URL = '/////translatorscafe.com/cafe/images/flags/{code}.gif'
# Templates Setting
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'website/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'notifications.views.count_notifications',
            ],
        },
    },
]

# WSGI App Setting
WSGI_APPLICATION = 'website.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password Validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
]


# Internationalization
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# For white noise
FILE_CHARSET = "utf-8"

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # When DEBUG==False

# Login URL
LOGIN_URL = 'khandiary:login'

LOGIN_REDIRECT_URL = 'core:index'

# Django by default danger message's tuning.
MESSAGE_TAGS = {
    message_constants.ERROR: 'danger',
}


# Log the user out after certain period of time.
#SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # opional, as this will log you out when browser is closed
SESSION_COOKIE_AGE = 7*24*60*60          # Log out after 7 days
SESSION_SAVE_EVERY_REQUEST = False      # Will prrevent from logging you out after 300 seconds
SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

# Email config
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtpout.secureserver.net'
EMAIL_HOST_USER = 'Khan Diary'
DEFAULT_FROM_EMAIL = 'your email'
EMAIL_HOST_PASSWORD = 'your password'
EMAIL_PORT = 587
EMAIL_USE_SSL = False
EMAIL_USE_TLS = True

DEFAULT_DOMAIN = 'http://{}'.format(ALLOWED_HOSTS[0])

# Password reset timeout
PASSWORD_RESET_TIMEOUT_MINUTES = "5"

APPEND_SLASH = True


# Website does not show any page if it is enabled
CONSTRUCTION = False
CONSTRUCTION_INFO = "down"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True