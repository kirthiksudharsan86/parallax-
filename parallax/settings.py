import sys
from pathlib import Path
from decouple import config
import dj_database_url
import os
BASE_DIR = Path(__file__).resolve().parent.parent
LOCAL_DEV_COMMANDS = {'runserver', 'test', 'check'}
IS_LOCAL_DEV_COMMAND = any(command in sys.argv for command in LOCAL_DEV_COMMANDS)
def get_debug_flag():
    raw_value = config('DEBUG', default='True')
    normalized = str(raw_value).strip().lower()
    if normalized in {'1', 'true', 'yes', 'on'}:
        return True
    if normalized in {'0', 'false', 'no', 'off', 'release', 'prod', 'production'}:
        return False
    return True
def get_staticfiles_storage():
    manifest_path = BASE_DIR / 'staticfiles' / 'staticfiles.json'
    if DEBUG or not manifest_path.exists():
        return 'django.contrib.staticfiles.storage.StaticFilesStorage'
    return 'whitenoise.storage.CompressedManifestStaticFilesStorage'
SECRET_KEY = config('DJANGO_SECRET_KEY', default='dev-insecure-change-in-production')
DEBUG = get_debug_flag()
ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS',
    default='parallax-production-2a2d.up.railway.app,parallax2026.in,localhost,127.0.0.1',
).split(',')
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False
CSRF_TRUSTED_ORIGINS = [
    "https://parallax-production-2a2d.up.railway.app",
    "https://parallax2026.in",
]
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'parallax',
    'core',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    #'core.security_shield.SecurityShieldMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF = 'parallax.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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
SITE_ID = 1
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
    )
}
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'security_shield_cache_table',
    }
}

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"
LOGIN_REDIRECT_URL = "auth_router"
LOGOUT_REDIRECT_URL = "home"
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_SIGNUP_FIELDS = ["email*"]
ACCOUNT_EMAIL_VERIFICATION = "none"
GOOGLE_CLIENT_ID = config("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = config("GOOGLE_CLIENT_SECRET")
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": [
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
        "APPS": [{
            "client_id": GOOGLE_CLIENT_ID,
            "secret": GOOGLE_CLIENT_SECRET,
            "key": "",
        }],
    }
}
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='placeholder.parallax@gmail.com')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='PLACEHOLDER_APP_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
REQUIRE_INVOICE_VERIFICATION = config('REQUIRE_INVOICE_VERIFICATION', default=False, cast=bool)
EVENT_HUB_URL = config('EVENT_HUB_URL', default='https://eventhubcc.vit.ac.in/EventHub/#:~:text=Parallax')
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = get_staticfiles_storage()
WHITENOISE_USE_FINDERS = DEBUG or IS_LOCAL_DEV_COMMAND
WHITENOISE_AUTOREFRESH = DEBUG or IS_LOCAL_DEV_COMMAND
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
SOCIALACCOUNT_LOGIN_ON_GET = True