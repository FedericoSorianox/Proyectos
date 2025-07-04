

from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv  # <-- AÑADE ESTA LÍNEA
import os

load_dotenv()  # <-- AÑADE ESTA LÍNEA


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-your-secret-key-here'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'badgers_project.urls'

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

WSGI_APPLICATION = 'badgers_project.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files
# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

# JWT settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}

# CORS settings
CORS_ALLOW_ALL_ORIGINS = True  # Only for development
CORS_ALLOW_CREDENTIALS = True

from corsheaders.defaults import default_headers
CORS_ALLOW_HEADERS = list(default_headers) + [
    'authorization',
] 
# ==============================================================================
# CONFIGURACIÓN DE ALMACENAMIENTO EN AWS S3
# ==============================================================================

# 1. Credenciales y configuración del Bucket
# ¡NUNCA pongas estas claves directamente en el código en producción! 
# Usa variables de entorno. Por ahora, para probar, puedes ponerlas aquí.
AWS_ACCESS_KEY_ID = 'TU_ACCESS_KEY_ID'
AWS_SECRET_ACCESS_KEY = 'TU_SECRET_ACCESS_KEY'
AWS_STORAGE_BUCKET_NAME = 'badgerss3' # El nombre que le diste a tu bucket
AWS_S3_REGION_NAME = 'sa-east-1' # O la región donde creaste el bucket (ej: 'sa-east-1')

# 2. Configuración del comportamiento de los archivos
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com'
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400', # Controla el caché del navegador por 1 día
}
AWS_DEFAULT_ACL = 'public-read' # Permite que los archivos subidos sean públicamente legibles

# 3. Ubicación de los archivos
# Los archivos de MEDIA (subidos por los usuarios) irán a la carpeta 'media/' dentro del bucket.
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
#DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# 4. (Opcional pero recomendado) Configuración para archivos estáticos (CSS, JS)
# Si en el futuro quieres servir también tus archivos estáticos desde S3.
# STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# ==============================================================================
# CONFIGURACIÓN DE ALMACENAMIENTO MODERNA (DJANGO 4.2+)
# ==============================================================================

# Los archivos de MEDIA (subidos por los usuarios) se manejarán con S3.
# Los archivos STATIC (CSS, JS) se seguirán manejando localmente.

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}