import os
import environ
from pathlib import Path

# Reading .env file
env = environ.Env()
environ.Env.read_env()

# Define the application directory
ROOT_DIR = environ.Path(__file__) - 2
CORE_DIR = ROOT_DIR.path('core')
BASE_DIR = Path(__file__).parent


SECRET_KEY = 'django-insecure-row7qk2h@57rh_pg)gdprmp6fwggm-59wunbk&5^aoerq*3t5n'

DEBUG = True

ALLOWED_HOSTS = [
  
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'utilisateurs',
    'gesthotel',
    'django.contrib.humanize',
    'guardian',
    'personnels',
    'services',
    'simple_history',
    'finances',
    'xhtml2pdf'
]

AUTH_USER_MODEL = 'utilisateurs.Utilisateurs'


MIDDLEWARE = [
    
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',

]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(ROOT_DIR, 'templates')],  # Chemin vers le dossier des templates
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'gesthotel.context_processors.notifications_toutes',


            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
  'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
    ]



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'logiciel_hotel',
        'USER': 'logiciel_hotel',
        'PASSWORD': 'logiciel_hotel',
        'HOST': 'localhost',  # Ou l'adresse IP de votre serveur MySQL
        'PORT': '3306',  # Port par défaut de MySQL
       'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}






# DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': BASE_DIR / 'db.sqlite3',
#    }
# }







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

LANGUAGE_CODE = 'fr-FR'

TIME_ZONE = 'Africa/Abidjan'

USE_I18N = True

USE_TZ = True

# Chemin vers le dossier racine d'upload des fichiers
MEDIA_ROOT = ROOT_DIR.path('static/media')

# URL publique pour accéder aux fichiers uploadés
MEDIA_URL = '/media/'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join('staticfiles')
STATICFILES_DIRS = [
    os.path.join('static'),
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp-relay.brevo.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'no-reply@avisconcours.com'
EMAIL_HOST_PASSWORD = '1Ik7v3wPRhJs8xVC'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'no-reply@avisconcours.com'
EMAIL_FROM_NAME = 'avisconcours'



SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_NAME = 'session_name'
SESSION_COOKIE_AGE = 12096  # Durée de vie du cookie de session en secondes (2 semaines)
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # True si la session expire lorsque le navigateur est fermé
SESSION_SAVE_EVERY_REQUEST = True  # True pour enregistrer la session à chaque requête
