from pathlib import Path

import environ
import os
import mimetypes
from datetime import timedelta

from django.urls import reverse_lazy


mimetypes.add_type("application/javascript", ".js", True)

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
DJANGO_LIVE_TEST_SERVER_ADDRESS="localhost:8000-8010,8080,9200-9300"
# Set the project base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# False ifnot in os.environ because of casting above
DEBUG = env('DEBUG')

# Raises Django's ImproperlyConfigured
# exception if SECRET_KEY not in os.environ
SECRET_KEY = env('SECRET_KEY')

# Parse database connection url strings
# like psql://user:pass@127.0.0.1:8458/db


if 'POSTGRES_USER' in os.environ:
    DATABASES = {
        # The db() method is an alias for db_url().
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': env('POSTGRES_DB'),
            'USER': env('POSTGRES_USER'),
            'HOST': env('POSTGRES_HOST'),
            'PORT': env('POSTGRES_PORT'),
            'PASSWORD':env('POSTGRES_PASS')
        }
    }
else:
    raise Exception('Add env variables for postgres!')

# TODO when adding cache
# CACHES = {
#     # Read os.environ['CACHE_URL'] and raises
#     # ImproperlyConfigured exception if not found.
#     #
#     # The cache() method is an alias for cache_url().
#     'default': env.cache(),

#     # read os.environ['REDIS_URL']
#     'redis': env.cache_url('REDIS_URL')
# }


ALLOWED_HOSTS = ['martial.fly.dev', '127.0.0.1', 'localhost:8000', 'localhost']
CSRF_TRUSTED_ORIGINS = ['https://*.martial.fly.dev', 'https://127.0.0.1:8000', 'https://127.0.0.1:9000']

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)
MANAGERS = ADMINS

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django_celery_beat',
    # apps

    'apps.customer_accounts',
    'apps.tickets',
    'apps.reviews',

    # libraries
    'django_multitenant',
    'environ',
    'debug_toolbar',
    'widget_tweaks',
    'django_extensions',
    'allauth',
    'allauth.account',
    'allauth.usersessions',
    'django_browser_reload',
    'django_htmx',
    "invitations",
    
]

TAILWIND_APP_NAME = 'theme'
ORGANIZATION_MODEL = 'workspace.Organization'
ORGANIZATION_USER_MODEL = 'workspace.OrganizationUser'
ORGANIZATION_OWNER_MODEL = 'workspace.OrganizationOwner'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'allauth.usersessions.middleware.UserSessionsMiddleware',
    'django_browser_reload.middleware.BrowserReloadMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
    'apps.customer_accounts.middleware.MultitenantMiddleware',
]

ROOT_URLCONF = 'limuza.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
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

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

WSGI_APPLICATION = 'limuza.wsgi.application'


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

LANGUAGE_CODE = 'en'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

INTERNAL_IPS = ["127.0.0.1", "0.0.0.0"]

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / "static"
]


STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
# WHITENOISE
WHITENOISE_USE_FINDERS = True
WHITENOISE_MANIFEST_STRICT = False
WHITENOISE_ALLOW_ALL_ORIGINS = True

# ALLAUTH
USERSESSIONS_TRACK_ACTIVITY = True
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
# PREFIX can be different for each env, can be set in .env
ACCOUNT_EMAIL_SUBJECT_PREFIX = env('ACCOUNT_EMAIL_SUBJECT_PREFIX', default='Martial:') + ' '
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
# ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 86400

# todo below: we should user url name, instead of hardcoded urls
# we might need to user reverse_lazy, not reverse
ACCOUNT_LOGOUT_REDIRECT_URL_NAME = 'account_login'
ACCOUNT_LOGOUT_REDIRECT_URL = reverse_lazy(ACCOUNT_LOGOUT_REDIRECT_URL_NAME)
LOGIN_REDIRECT_URL_NAME = 'show_dashboard'
LOGIN_REDIRECT_URL = reverse_lazy(LOGIN_REDIRECT_URL_NAME)  # default to /accounts/profile view from allauth

# after time lapses, when user tries to click somewhere in the page he gets logged out
# default in django is 2 weeks in seconds (1209600)
SESSION_COOKIE_AGE = int(
    env('SESSION_COOKIE_AGE', default=timedelta(days=7).total_seconds()))

# django-invitations
ACCOUNT_ADAPTER = "invitations.models.InvitationsAdapter"
INVITATIONS_ADAPTER = ACCOUNT_ADAPTER
INVITATIONS_ADMIN_ADD_FORM = "apps.customer_accounts.forms.CustomInvitationAdminAddForm"
INVITATIONS_INVITATION_MODEL = "customer_accounts.CustomInvitation"

# how many days for the invitation to expire, default 3
INVITATIONS_INVITATION_EXPIRY = 7

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Logging configuration for production
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'django_error.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

# API KEYS
ASSEMBLY_AI_API_KEY = env('ASSEMBLY_AI_API_KEY')
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda _request: DEBUG
}

# sends email to console in development, otherwises sends real emails to users

DEVELOPMENT = env('DEVELOPMENT') if 'DEVELOPMENT' in os.environ else False


if DEVELOPMENT:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    DEFAULT_FROM_EMAIL = env('EMAIL_HOST_USER') if 'EMAIL_HOST_USER' in os.environ else 'example@example.com'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_USE_TLS = True
    EMAIL_PORT = 587
    EMAIL_HOST = env('EMAIL_HOST')
    EMAIL_HOST_USER = env('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASS')
    DEFAULT_FROM_EMAIL = env('EMAIL_HOST_USER')

# Celery Settings
CELERY_BROKER_URL = 'redis://redis:6379/0'  # or your broker URL
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'  # or your result backend
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'  # or your timezone
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'