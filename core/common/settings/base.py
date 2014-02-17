# -*- coding: utf-8 -*-

# Django base settings for common core.

from os.path import dirname, join

import core
#import lsst
#import atlas

ADMINS = (
    ('Jaroslava Schovancova', 'jschovan@gmail.com'),
)
MANAGERS = ADMINS


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Site ID
SITE_ID = 1


# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',  # for AJAX POST protection with csrf
    'django.contrib.auth.middleware.AuthenticationMiddleware',
### added
    'django.contrib.auth.middleware.RemoteUserMiddleware',  # for APIs: htcondorapi
### END added
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
###
#    'django.middleware.common.CommonMiddleware',
#    'django.contrib.sessions.middleware.SessionMiddleware',
#    'django.middleware.csrf.CsrfViewMiddleware',  # for AJAX POST protection with csrf
#    'django.contrib.auth.middleware.AuthenticationMiddleware',
#    'django.contrib.messages.middleware.MessageMiddleware',
#    # Uncomment the next line for simple clickjacking protection:
#    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'core.common.urls'

### added
TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    join(dirname(core.common.__file__), 'templates'),
)


# installed apps
INSTALLED_APPS_DJANGO_FRAMEWORK = (
    ### Django framework
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)
INSTALLED_APPS_DJANGO_PLUGINS = (
    ### Django plugins
    'rest_framework',  #pip install djangorestframework, version 2.3.10
    'django_datatables_view',  #pip install django-datatables-view, version 1.6
)
INSTALLED_APPS_BIGPANDAMON_CORE = (
    ### BigPanDAmon core
    'core.common',
    'core.table',
#    'core.graphics', #NOT-IMPLEMENTED
    'core.pandajob',
    'core.resource',
    'core.htcondor',
#    'core.task', #NOT-IMPLEMENTED
)
COMMON_INSTALLED_APPS = \
    INSTALLED_APPS_DJANGO_FRAMEWORK + \
    INSTALLED_APPS_DJANGO_PLUGINS
INSTALLED_APPS = COMMON_INSTALLED_APPS + INSTALLED_APPS_BIGPANDAMON_CORE


VERSION = core.common.__versionstr__

VERSIONS = {
    'core': core.__versionstr__,
#    'lsst': lsst.__versionstr__,
#    'atlas': atlas.__versionstr__,
}

