"""
    logconfig
"""

from .local import LOG_ROOT

# init logger
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
#LOG_ROOT = '/data/bigpandamon_virtualhosts/atlas/logs/'
LOG_SIZE = 1000000000
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
#    'disable_existing_loggers': True,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'logfile-django': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': LOG_ROOT + "/logfile.django",
            'maxBytes': LOG_SIZE,
            'backupCount': 2,
            'formatter': 'verbose',
        },
        'logfile-viewdatatables': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': LOG_ROOT + "/logfile.viewdatatables",
            'maxBytes': LOG_SIZE,
            'backupCount': 2,
            'formatter': 'verbose',
        },
        'logfile-rest': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': LOG_ROOT + "/logfile.rest",
            'maxBytes': LOG_SIZE,
            'backupCount': 2,
            'formatter': 'verbose',
        },
        'logfile-bigpandamon': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': LOG_ROOT + "/logfile.bigpandamon",
            'maxBytes': LOG_SIZE,
            'backupCount': 2,
            'formatter': 'verbose',
        },
        'logfile-jedi_jobsintask': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': LOG_ROOT + "/logfile.jedi_jobsintask",
            'maxBytes': LOG_SIZE,
            'backupCount': 2,
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
#            'class': 'django.utils.log.AdminEmailHandler'
            'class':'logging.StreamHandler',
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
#            'level': 'ERROR',
            'level': 'DEBUG',
            'propagate': True,
        },
        'django': {
            'handlers':['logfile-django'],
            'propagate': True,
            'level':'DEBUG',
        },
        'django_datatables_view': {
            'handlers':['logfile-viewdatatables'],
            'propagate': True,
            'level':'DEBUG',
        },
        'rest_framework': {
            'handlers':['logfile-rest'],
            'propagate': True,
            'level':'DEBUG',
        },
        'bigpandamon': {
            'handlers': ['logfile-bigpandamon'],
            'level': 'DEBUG',
        },
        'jedi_jobsintask': {
            'handlers': ['logfile-jedi_jobsintask'],
            'level': 'DEBUG',
        },
    },
    'formatters': {
        'verbose': {
#            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
            'format': '%(asctime)s %(module)s %(name)-12s:%(lineno)d %(levelname)-5s %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(name)-12s:%(lineno)d %(message)s'
        },
    },
    'logfile': {
        'level':'DEBUG',
        'class':'logging.handlers.RotatingFileHandler',
        'filename': LOG_ROOT + "/logfile",
        'maxBytes': LOG_SIZE,
        'backupCount': 5,
        'formatter': 'verbose',
    },
}


