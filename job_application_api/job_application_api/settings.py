"""
Django settings for job_application_api project.

IMPORTANT SETTINGS EXPLAINED:
==============================
1. INSTALLED_APPS: List of all Django apps (both built-in and custom)
2. REST_FRAMEWORK: Configuration for Django REST Framework
3. SIMPLE_JWT: Configuration for JWT authentication
4. MEDIA settings: For handling file uploads (resumes)
5. Database: SQLite (simple file-based database, good for development)

For production, you should:
- Use PostgreSQL/MySQL instead of SQLite
- Move SECRET_KEY to environment variables
- Set DEBUG = False
- Configure ALLOWED_HOSTS properly
"""

from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-s_d0#)pc=jv1olzp6-r&*#uhb48$*&=3)0l18m6$s*nqkn9b9o"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition
# INSTALLED_APPS: All apps that are active in this project

INSTALLED_APPS = [
    # Django built-in apps (admin panel, authentication, etc.)
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    
    # Third-party apps
    # Django REST Framework - for building APIs
    "rest_framework",
    
    # Django Filter - for filtering and searching
    "django_filters",
    
    # Our custom apps
    # These are the apps we created with 'startapp' command
    "applicants",      # Manages applicants
    "jobs",           # Manages job postings
    "applications",   # Manages job applications
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "job_application_api.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "job_application_api.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ==============================================================================
# DJANGO REST FRAMEWORK CONFIGURATION
# ==============================================================================
# This configures how the REST API behaves

REST_FRAMEWORK = {
    # Authentication: How we verify who is making the request
    # JWTAuthentication: Uses JWT tokens (from Authorization header)
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    
    # Permissions: Who can access the API
    # IsAuthenticated: Must have valid JWT token
    # You can override this per-view if needed
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    
    # Pagination: How many items to show per page in list views
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,  # 10 items per page
    # Usage: /api/applicants/?page=2 to get second page
    
    # Filter backends: For searching and filtering
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    
    # Response format
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',  # JSON responses
        'rest_framework.renderers.BrowsableAPIRenderer',  # Web UI for testing
    ],
}


# ==============================================================================
# JWT (JSON Web Token) CONFIGURATION
# ==============================================================================
# JWT is a secure way to authenticate users with tokens

SIMPLE_JWT = {
    # How long an access token is valid
    # Access tokens are short-lived for security
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    
    # How long a refresh token is valid
    # Refresh tokens are used to get new access tokens
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    
    # Whether to rotate refresh tokens (create new one on refresh)
    'ROTATE_REFRESH_TOKENS': True,
    
    # Whether to blacklist refresh tokens after rotating
    'BLACKLIST_AFTER_ROTATION': True,
    
    # Algorithm used to sign the JWT
    'ALGORITHM': 'HS256',
    
    # The signing key (uses Django's SECRET_KEY)
    'SIGNING_KEY': SECRET_KEY,
    
    # Header type
    'AUTH_HEADER_TYPES': ('Bearer',),
    # Usage: Authorization: Bearer <your-token-here>
}


# ==============================================================================
# MEDIA FILES CONFIGURATION
# ==============================================================================
# For handling uploaded files (like resumes)

# URL prefix for media files
# Example: http://localhost:8000/media/resumes/resume.pdf
MEDIA_URL = '/media/'

# Directory where uploaded files are stored
MEDIA_ROOT = BASE_DIR / 'media'


# ==============================================================================
# CORS CONFIGURATION (Optional - for frontend integration)
# ==============================================================================
# If you have a separate frontend (React, Vue, etc.), uncomment these:

# INSTALLED_APPS += ['corsheaders']
# MIDDLEWARE.insert(0, 'corsheaders.middleware.CorsMiddleware')
# CORS_ALLOW_ALL_ORIGINS = True  # For development only!
# For production, specify allowed origins:
# CORS_ALLOWED_ORIGINS = ['http://localhost:3000', 'https://yourfrontend.com']
