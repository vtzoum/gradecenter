#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Django settings for bk043 project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
#Update.1 to support Jinja2 @ 20161021 
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
import jinja2

# TIME ZONE ERROR
import warnings
import exceptions
#warnings.filterwarnings("ignore", category=exceptions.RuntimeWarning, module='django.db.backends.sqlite3.base', lineno=53)


#default
#BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=ts@$czg@*^ruqv1z319&n8an*9dh2pxo@%_+_7_*)jz@i(d4('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
#DEBUG = False
#TEMPLATE_DEBUG = DEBUG
ALLOWED_HOSTS = ['*']
#ALLOWED_HOSTS = ['localhost', '127.0.0.1', '111.222.333.444', 'mywebsite.com']
#ALLOWED_HOSTS = []

###################################
# Application definition
###################################
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'registration',      #REDUX
    'django.contrib.admin',
    # 'django.contrib.admindocs',
    'bk043',
    'personel', 
    #'accounts', 
    'user_profile',      # Custom User_profile
    'reporting', 
    #'apps.main.middleware.AjaxMessaging'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

     #vtzoum-middleware > add here our custom middleware
     'middleware.ajaxmessages.AjaxMessaging',
     #'middleware.authenticate.AuthRequiredMiddleware'

)

###################################
# URL_CONF
###################################
ROOT_URLCONF = 'bk043.urls'

###################################
# CONTEXT_PROCESSORS 
# vtzoum to support jinja2 auth @ 20191021
###################################
_CONTEXT_PROCESSORS = [
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'session_csrf.context_processor',
    'fjord.base.context_processors.globals',
    'fjord.base.context_processors.i18n',
]

###################################
# TEMPLATES
###################################
TEMPLATES = [
    #Update.1 to support Jinja2 @ 20161021 
    
    { 
        'BACKEND':'django.template.backends.jinja2.Jinja2',
        'DIRS': [
            #'%s/templates.jinja/'% (PROJECT_DIR),
            "%s/templates.jinja" % BASE_DIR,
            ],
        'APP_DIRS': True,
        'OPTIONS': {
            #Update.B2 to support xxx @ 20161021 
            #'match_extension': '',
            #'match_extension': '.jinja',
            #'newstyle_gettext': True,
            #'context_processors': _CONTEXT_PROCESSORS,
            
            #Update.B0 @ 20161021 
            'autoescape': False,
            'undefined':jinja2.StrictUndefined,
            'environment': 'bk043.jinja.env.JinjaEnvironment',
            #Update.B1 to support Jinja2 extensions @ 20161021 
            'extensions': [
                'jinja2.ext.loopcontrols',
                'jdj_tags.extensions.DjangoCompat',
                #Update.B2 to support Jinja2 CUSTOM extensions @ 20161021 
                #'bk043.jinja.extensions.DjangoNow',

                #Update.B3 to support Jinja2 XXX @ 20161021 
                'jinja2.ext.do',
                'jinja2.ext.with_',
                'jinja2.ext.autoescape',
                #'django_jinja.builtins.extensions.CsrfExtension',
                #'django_jinja.builtins.extensions.StaticFilesExtension',
                #'django_jinja.builtins.extensions.DjangoFiltersExtension',
                #'fjord.base.l10n.MozInternationalizationExtension',
                #'pipeline.templatetags.ext.PipelineExtension',                
                ],            
        },        
        }, #JINJ2 support        
    
    #default
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
        # Always use forward slashes, even on Windows.
        # Don't forget to use absolute paths, not relative paths.
        'DIRS': [
            '/home/html/example.com', 
            "%s/templates" % BASE_DIR,
            ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],#context_processors

	    'builtins': [
                 'personel.templatetags.template_filters',
                 #'coffeehouse.builtins',
            ],#builtins

        },#OPTIONS
    }, # TEMPLATES
]


TEMPLATE_DEBUG = True

###################################
# Application definition
###################################
WSGI_APPLICATION = 'bk043.wsgi.application'

###################################
# Database
###################################
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        #'NAME': os.path.join(BASE_DIR, 'dbDemo-2018.sqlite3'),
        #'NAME': os.path.join(BASE_DIR, 'dbBK043_2017.sqlite3'),
    }
}

###################################
# Internationalization
###################################
# https://docs.djangoproject.com/en/1.7/topics/i18n/
LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True
#
USE_TZ = False  #step2. conflicts with sqlite3. comment out after ... migrate
#USE_TZ = True  #step1. favors sqlite3. use in ...makemigrations+migrate
TIME_ZONE = 'Europe/Athens'   # SOS.required for correct time in grid
#TIME_ZONE = 'UTC'

###################################
# MEDIA root for model-based (;)UPLOADS
###################################
#The MEDIA_ROOT is the path on the filesystem to the directory containing your static media.
#The MEDIA_URL is the URL that makes the static media accessible over HTTP.
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


###################################
# Static files (CSS, JavaScript, Images)
###################################
# https://docs.djangoproject.com/en/1.7/howto/static-files/
ROOT_PATH = os.path.dirname(__file__)


#Set the STATIC_ROOT setting to point to the filesystem path 
#you'd like your static files collected when you use the collectstatic management command"
#Development
#STATIC_ROOT = os.path.join(BASE_DIR, "static/")
#STATIC_URL = '/static/'
#Production@APACHE2
#STATIC_ROOT = os.path.join(BASE_DIR, "../static")

#Development
#STATIC_ROOT = os.path.join(BASE_DIR)
#STATIC_URL = '/static/'
#STATIC_ROOT = os.path.join(BASE_DIR)
#STATIC_URL = 'http://mydomain/static/'


#Production@APACHE2
#STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_ROOT = os.path.join(BASE_DIR)
STATIC_URL = '/static/'
#STATIC_URL = 'http://mydomain/static/'
#OLD-probalby Wrong : STATIC_ROOT = os.path.join(BASE_DIR, "static/")


#STATICFILES_DIRS is a setting you use to declare non app-specific static files live in your project
#STATICFILES_DIRS = (BASE_DIR, 'static')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    #'/static/',    
    #'/var/www/static/',
]


# UPLOAD root for UPLOADed files 
UPLOAD_DIR = os.path.join(BASE_DIR, 'uploads')


# VTZOUM on Error <Model: Object> is not JSON serializable
#SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

###################################
# USER AUTH 
###################################
ACCOUNT_ACTIVATION_DAYS = 7     # One-week activation window; you may, of course, use a different value.
LOGIN_REDIRECT_URL = '/'  # The page you want users to arrive at after they successful log in
LOGIN_URL = '/accounts/login/'  # The page users are directed to if they are not logged in,
REGISTRATION_AUTO_LOGIN = True  # If True, the user will be automatically logged in.
LOGIN_REDIRECT_VIEW = 'loginSuccess'
REGISTRATION_OPEN = True                # If True, users can register 
# and are trying to access pages requiring authentication
                                                               

#2017 April >> Untested
"""
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}
"""


###################################
# VTZOUM APP CONSTANTS
###################################
CONST_FOLDERBOOKS=25               #Books/Folder    (eg. Full Folder has 25 books)
CONST_MINFOLDERBOOKS=4             #Books    (eg. Folder has at least 4 books)
CONST_MAXACTIONDURATION=3          #Days     (eg. keep folder max 3 days)
##REPORTING
CONST_REPORTS_GCENTER_NAME=u"43ο ΒΚ ΑΓΡΙΝΙΟY"                #
CONST_REPORTS_GCENTER_PRESIDENT_ARTICLE=u"o"                 #
CONST_REPORTS_GCENTER_PRESIDENT_NAME=u"ΒΑΣΙΛΕΙΟΣ"            #
CONST_REPORTS_GCENTER_PRESIDENT_SURNAME=u"ΤΖΟΥΜΑΚΑΣ"         #

