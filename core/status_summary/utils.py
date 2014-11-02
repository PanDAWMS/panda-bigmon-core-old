"""
    status_summary.utils
    
"""
import logging
import pytz
from datetime import datetime, timedelta

from django.db.models import Count, Sum

_logger = logging.getLogger('bigpandamon')


defaultDatetimeFormat = '%Y-%m-%dT%H:%M:%S'


def configure(request_GET):
    errors_GET = {}
    ### if startdate&enddate are provided, use them
    if 'startdate' in request_GET and 'enddate' in request_GET:
        nhours = -1
        ### startdate
        startdate = request_GET['startdate']
        try:
            dt_start = datetime.strptime(startdate, defaultDatetimeFormat)
        except ValueError:
            errors_GET['startdate'] = \
                'Provided startdate [%s] has incorrect format, expected [%s].' % \
                (startdate, defaultDatetimeFormat)
            startdate = datetime.utcnow() - timedelta(hours=nhours)
            startdate = startdate.replace(tzinfo=pytz.utc).strftime(defaultDatetimeFormat)
        ### enddate
        enddate = request_GET['enddate']
        try:
            dt_end = datetime.strptime(enddate, defaultDatetimeFormat)
        except ValueError:
            errors_GET['enddate'] = \
                'Provided enddate [%s] has incorrect format, expected [%s].' % \
                (enddate, defaultDatetimeFormat)
            enddate = datetime.utcnow()
            enddate = enddate.replace(tzinfo=pytz.utc).strftime(defaultDatetimeFormat)
    ### if nhours is provided, do query "last N days"
    elif 'nhours' in request_GET:
        try:
            nhours = int(request_GET['nhours'])
        except:
            nhours = 12
            errors_GET['nhours'] = \
                'Wrong or no nhours has been provided.Using [%s].' % \
                (nhours)
        startdate = datetime.utcnow() - timedelta(hours=nhours)
        startdate = startdate.replace(tzinfo=pytz.utc).strftime(defaultDatetimeFormat)
        enddate = datetime.utcnow()
        enddate = enddate.replace(tzinfo=pytz.utc).strftime(defaultDatetimeFormat)
    ### neither nhours, nor startdate&enddate was provided
    else:
        nhours = 12
        startdate = datetime.utcnow() - timedelta(hours=nhours)
        startdate = startdate.replace(tzinfo=pytz.utc).strftime(defaultDatetimeFormat)
        enddate = datetime.utcnow()
        enddate = enddate.replace(tzinfo=pytz.utc).strftime(defaultDatetimeFormat)
        errors_GET['noparams'] = \
                'Neither nhours, nor startdate & enddate has been provided. Using startdate=%s and enddate=%s.' % \
                (startdate, enddate)

    return startdate, enddate, nhours, errors_GET


