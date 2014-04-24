from tempfile import gettempdir
from os.path import dirname, join

from core import common

DEBUG = True
#DEBUG = False
TEMPLATE_DEBUG = DEBUG

#### django-debug-toolbar
#INTERNAL_IPS = ['24.191.185.49']

ALLOWED_HOSTS = [
    ### cern.ch
    '.cern.ch',  # Allow domain and subdomains
    '.cern.ch.',  # Also allow FQDN and subdomains
    ### bigpanda.cern.ch
    'bigpanda.cern.ch',  # Allow domain and subdomains
    'bigpanda.cern.ch.',  # Also allow FQDN and subdomains
    ### pandawms.org
    '.pandawms.org',  # Allow domain and subdomains
    '.pandawms.org.',  # Also allow FQDN and subdomains
]

# Make this unique, and don't share it with anybody.
from .local import dbaccess, MY_SECRET_KEY, defaultDatetimeFormat
SECRET_KEY = MY_SECRET_KEY
# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = dbaccess

## init logger
## A sample logging configuration. The only tangible logging
## performed by this configuration is to send an email to
## the site admins on every HTTP 500 error when DEBUG=False.
## See http://docs.djangoproject.com/en/dev/topics/logging for
## more details on how to customize your logging configuration.
from .logconfig import LOGGING
##LOG_ROOT = '/data/bigpandamon_virtualhosts/atlas/logs/'
#LOG_SIZE = 1000000000
#LOGGING = {
#    'version': 1,
#    'disable_existing_loggers': False,
##    'disable_existing_loggers': True,
#    'filters': {
#        'require_debug_false': {
#            '()': 'django.utils.log.RequireDebugFalse'
#        }
#    },
#    'handlers': {
#        'null': {
#            'level':'DEBUG',
#            'class':'django.utils.log.NullHandler',
#        },
#        'logfile-bigpandamon': {
#            'level':'DEBUG',
#            'class':'logging.handlers.RotatingFileHandler',
#            'filename': LOG_ROOT + "/logfile.bigpandamon",
#            'maxBytes': LOG_SIZE,
#            'backupCount': 2,
#            'formatter': 'verbose',
#        },
#        'logfile-django': {
#            'level':'DEBUG',
#            'class':'logging.handlers.RotatingFileHandler',
#            'filename': LOG_ROOT + "/logfile.django",
#            'maxBytes': LOG_SIZE,
#            'backupCount': 2,
#            'formatter': 'verbose',
#        },
#        'logfile-viewdatatables': {
#            'level':'DEBUG',
#            'class':'logging.handlers.RotatingFileHandler',
#            'filename': LOG_ROOT + "/logfile.viewdatatables",
#            'maxBytes': LOG_SIZE,
#            'backupCount': 2,
#            'formatter': 'verbose',
#        },
#        'logfile-rest': {
#            'level':'DEBUG',
#            'class':'logging.handlers.RotatingFileHandler',
#            'filename': LOG_ROOT + "/logfile.rest",
#            'maxBytes': LOG_SIZE,
#            'backupCount': 2,
#            'formatter': 'verbose',
#        },
#        'logfile-jedi_jobsintask': {
#            'level':'DEBUG',
#            'class':'logging.handlers.RotatingFileHandler',
#            'filename': LOG_ROOT + "/logfile.jedi_jobsintask",
#            'maxBytes': LOG_SIZE,
#            'backupCount': 2,
#            'formatter': 'verbose',
#        },
#        'mail_admins': {
#            'level': 'ERROR',
#            'filters': ['require_debug_false'],
##            'class': 'django.utils.log.AdminEmailHandler'
#            'class':'logging.StreamHandler',
#        }
#    },
#    'loggers': {
#        'django.request': {
#            'handlers': ['mail_admins'],
##            'level': 'ERROR',
#            'level': 'DEBUG',
#            'propagate': True,
#        },
#        'django': {
#            'handlers':['logfile-django'],
#            'propagate': True,
#            'level':'DEBUG',
#        },
#        'django_datatables_view': {
#            'handlers':['logfile-viewdatatables'],
#            'propagate': True,
#            'level':'DEBUG',
#        },
#        'rest_framework': {
#            'handlers':['logfile-rest'],
#            'propagate': True,
#            'level':'DEBUG',
#        },
#        'bigpandamon': {
#            'handlers': ['logfile-bigpandamon'],
#            'level': 'DEBUG',
#        },
#        'jedi_jobsintask': {
#            'handlers': ['logfile-jedi_jobsintask'],
#            'level': 'DEBUG',
#        },
#    },
#    'formatters': {
#        'verbose': {
##            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
#            'format': '%(asctime)s %(module)s %(name)-12s:%(lineno)d %(levelname)-5s %(message)s'
#        },
#        'simple': {
#            'format': '%(levelname)s %(name)-12s:%(lineno)d %(message)s'
#        },
#    },
#    'logfile': {
#        'level':'DEBUG',
#        'class':'logging.handlers.RotatingFileHandler',
#        'filename': LOG_ROOT + "/logfile",
#        'maxBytes': LOG_SIZE,
#        'backupCount': 5,
#        'formatter': 'verbose',
#    },
#}

# media
# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
#MEDIA_ROOT = '/data/bigpandamon/bigpandamon/media/'
MEDIA_ROOT = "/data/bigpandamon_virtualhosts/jedimon/jedimon-core/core/common/media/"

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
#MEDIA_URL_BASE = '/media/'
#MEDIA_URL_BASE = '/media-common/'
MEDIA_URL_BASE = '/jedimonmedia/'


# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
#STATIC_ROOT = '/data/bigpandamon/bigpandamon/static/'
STATIC_ROOT = "/data/bigpandamon_virtualhosts/jedimon/jedimon-core/core/common/static/"

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
#STATIC_URL_BASE = '/static/'
#STATIC_URL_BASE = '/static-common/'
STATIC_URL_BASE = '/jedimonstatic/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    join(dirname(common.__file__), 'static'),
)


#SERVER_INFO = {
#    'type': 'dev',
#}


### VIRTUALENV
VIRTUALENV_PATH = '/data/virtualenv/django1.6.1__python2.6.6__atlas'
#VIRTUALENV_PATH = '/data/virtualenv/django1.6.1__python2.6.6__jedimon'

### WSGI
#WSGI_PATH = VIRTUALENV_PATH + '/bigpandamon'
WSGI_PATH = VIRTUALENV_PATH + '/jedimon'
#WSGI_PATH = VIRTUALENV_PATH + '/'

### topology
SOURCE_SCHEDCONFIG = {
    'lsst': 'http://atlas-agis-api.cern.ch/request/pandaqueue/query/list/?json&preset=schedconf.all&site_state=ANY&vo_name=lsst',
}

### jobs by ProdUserName
CUSTOM_DB_FIELDS = {
    'jobListByProdUser': {
        'jobparam': ['jobStatus', 'cpuConsumptionTime', 'creationTime', \
                     'startTime', 'endTime', 'modificationHost', 'computingSite', \
                     'prodUserName'], \
        'configurable': ['jobparam', 'prodUserName', 'days']
    }
}

### URL_PATH_PREFIX for multi-developer apache/wsgi instance
### on EC2: URL_PATH_PREFIX = '/bigpandamon' or URL_PATH_PREFIX = '/developersprefix'
#URL_PATH_PREFIX = '/bigpandamon-common'
#URL_PATH_PREFIX = '/jedimon'
#URL_PATH_PREFIX = ''
### on localhost:8000: URL_PATH_PREFIX = '/.'
URL_PATH_PREFIX = '/jedimon'
#URL_PATH_PREFIX = ''
#MEDIA_URL = URL_PATH_PREFIX + MEDIA_URL
MEDIA_URL = URL_PATH_PREFIX + MEDIA_URL_BASE
STATIC_URL = URL_PATH_PREFIX + STATIC_URL_BASE

ENV = {
    ### Application name
#    'APP_NAME': "ProdSys2", \
    'APP_NAME': "BigPanDA", \
    ### Page title default
    'PAGE_TITLE': "BigPanDA Monitor", \
    ### Menu item separator
    'SEPARATOR_MENU_ITEM': "&nbsp;&nbsp;&nbsp;", \
    ### Navigation chain item separator
    'SEPARATOR_NAVIGATION_ITEM': "&nbsp;&#187;&nbsp;" , \
}

FILTER_UI_ENV = {
    ### default number of days of shown jobs active in last N days
    'DAYS': 1, \
    ### default number of days for user activity of shown jobs active in last N days
    'USERDAYS': 3, \
    ### max number of days of shown jobs active in last N days
    'MAXDAYS': 30, \
    ### max number of days for user activity of shown jobs active in last N days
    'USERMAXDAYS': 60, \
    ### default number of hours of shown jobs active in last N hours
    'HOURS': 2, \
    ### wildcard for string pattern in filter form
    'WILDCARDS': ['*'], \
    ### wildcard for integer interval in filter form
    'INTERVALWILDCARDS': [':'], \
    ###
    'EXPAND_BUTTON': { "mDataProp": None, "sTitle": "Details", \
                       "sClass": "control center", "bVisible": True, \
                       "bSortable": False, \
                       "sDefaultContent": '<img src="' + STATIC_URL + \
                                '/images/details_open.png' + '">' \
            }, \
}

#TODO:
#CSRF_FAILURE_VIEW

