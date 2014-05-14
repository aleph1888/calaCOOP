#encoding=utf-8

"""
Django settings for ContaCIC project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '------------------'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Invoices',
    'south',
    'django_cron',
    'csvimport',
    'localflavor'
)

#https://pypi.python.org/pypi/django-csvimport
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
)

TEMPLATE_CONTEXT_PROCESSORS = (
	"django.contrib.auth.context_processors.auth",
	"django.core.context_processors.debug",
	"django.core.context_processors.i18n",
	"django.core.context_processors.media",
	"django.core.context_processors.static",
	"django.core.context_processors.tz",
	"django.contrib.messages.context_processors.messages"
)

DEFAULT_INDEX_TABLESPACE = 'indexes'



ROOT_URLCONF = 'ContaCIC.urls'

WSGI_APPLICATION = 'ContaCIC.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '-------------',
        'USER' : '----------',
        'PASSWORD': '-------',
        'HOST': 'localhost',
    }
}

CSVIMPORT_MODELS = ["Invoices.periodTaxes", 
		"Invoices.SalesInvoices",
		"Invoices.PurchaseInvoices",
		"Invoices.PeriodClose",
		"Invoices.Client",
		"Invoices.Provider",
		"Invoices.period",
		"Invoices.PaymentEntities",
		"Invoices.Coop",
		"Invoices.RefundEntities"]



# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/


import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]
PROJECT_PATH = os.path.dirname(os.path.dirname(__file__))

MEDIA_BASE = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, MEDIA_BASE)
MEDIA_URL = '/media/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "Invoices"),
		PROJECT_PATH + '/Invoices/templates/',
)
LANGUAGE_CODE = 'ca-ES'

LOCALE_PATHS = ( PROJECT_PATH + "/locale/",)

LANGUAGES = (
		('ca', 'Català'),
		('es', 'Castellano'),
	)
DECIMAL_SEPARATOR = ','
USE_THOUSAND_SEPARATOR = True
THOUSAND_SEPARATOR = '.'
TIME_ZONE = 'UTC'
USE_L10N = True
USE_I18N = True
USE_TZ = True

#Mail
EMAIL_HOST = "----------------t"
EMAIL_PORT = "25" 
EMAIL_HOST_USER = "----------" 
EMAIL_HOST_PASSWORD = ""
EMAIL_USE_TLS = False 
EMAIL_USE_SSL  = False
DEFAULT_FROM_EMAIL = "-----------"


USE_TZ = True


CRON_CLASSES = [
    "cron.EmailsNotifierCron",
    "cron.PeriodCloseAutomaticClose"
]
 

CRONJOBS = [
    ('*/1 * * * *', 'ContaCIC.cron')
]


