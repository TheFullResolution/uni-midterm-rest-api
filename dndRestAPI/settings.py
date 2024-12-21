from pathlib import Path
import environ
import os

# Initialize environment variables
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env')

# Security and Debug Settings
SECRET_KEY = env("SECRET_KEY", default="dummy-secret-key-for-dev")  # Secret key for encryption
DEBUG = env.bool("DEBUG", default=False)  # Enable debug mode in development

# Allowed Hosts and CSRF Configuration
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.fly.dev']  # Hosts allowed to serve the application
CSRF_TRUSTED_ORIGINS = ['https://*.fly.dev']  # Trusted origins for CSRF protection

# Application Definition
INSTALLED_APPS = [
    # Default Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'rest_framework',  # Django REST framework for API development

    # Local apps
    'dndRestAPI',  # Project-specific app
    'api',  # API app for handling endpoints
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URL Configuration
ROOT_URLCONF = 'dndRestAPI.urls'

# Template Configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,  # Automatically discover templates in installed apps
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

# WSGI Application
WSGI_APPLICATION = 'dndRestAPI.wsgi.application'

# Database Configuration
# Default to SQLite, can be overridden via DATABASE_URL in the .env file
DATABASES = {
    'default': env.db('DATABASE_URL', default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}")
}

# Password Validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Localization Settings
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static Files Configuration
STATIC_URL = 'static/'  # URL prefix for serving static files
STATICFILES_DIRS = [
    BASE_DIR / 'static',  # This ensures the 'static' folder is included in collectstatic
]
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Directory to collect static files for production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'  # Optimize static file delivery

# Redirect URLs for Login and Logout
LOGIN_REDIRECT_URL = '/'  # Redirect after successful login
LOGOUT_REDIRECT_URL = '/'  # Redirect after logout

# Default Primary Key Field Type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
