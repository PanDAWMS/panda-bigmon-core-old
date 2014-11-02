"""
    status_summary.utils
    
"""
import logging
import pytz
from datetime import datetime, timedelta

from django.db.models import Count, Sum

from lsst.views import statelist as STATELIST


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


def sort_data_by_cloud(data):
    """
        sort_data_by_cloud
        
        data: list of dictionaries
                    one dictionary per PanDA resource (computingsite)
                    keys: 
                        cloud
                        computingsite
                        and a bunch of other keys by job status, see STATELIST
        
        returns: input data sorted by cloud, computingsite
    """
    res = sorted(data, key=lambda x: (str(x['cloud']).lower(), \
                                      str(x['computingsite']).lower()))
    print res
    return res

def summarize_data(data):
    """
        summarize_data
        
        data: queryset, list of dictionaries, e.g. 
            [{'njobs': 1, 'computingsite': u'CERN-PROD', 'jobstatus': u'holding'}]
        
        returns: list of dictionaries
                    one dictionary per PanDA resource (computingsite)
                    keys: 
                        cloud
                        computingsite
                        and a bunch of other keys by job status, see STATELIST
    """
    result = []
    ### get list of computing sites
    computingsites = list(set([x['computingsite'] for x in data]))
    ### loop through computing sites, sum njobs for each job status
    for computingsite in computingsites:
        item={'computingsite': computingsite}
        # TODO: add topology info
        ### get records for this computingsite
        rec = [x for x in data \
               if x['computingsite'] == computingsite]
        ### get cloud for this computingsite
        cloud = ','.join(list(set([x['cloud'] for x in data \
                 if x['computingsite'] == computingsite])))
        item['cloud'] = cloud
        ### get njobs per jobstatus for this computingsite
        for jobstatus in STATELIST:
            jobstatus_rec = [x['njobs'] for x in rec \
                             if x['jobstatus'] == jobstatus]
            item[jobstatus] = sum(jobstatus_rec)
        ### store info for this computingsite
        result.append(item)
    ### sort result
    result = sort_data_by_cloud(result)
    return result




