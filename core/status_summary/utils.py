"""
    status_summary.utils
    
"""
import logging
import pytz
from datetime import datetime, timedelta

from django.db.models import Count, Sum
from ..resource.models import Schedconfig
from lsst.views import statelist as STATELIST


_logger = logging.getLogger('bigpandamon')


defaultDatetimeFormat = '%Y-%m-%dT%H:%M:%S'


def configure(request_GET):
    errors_GET = {}
    ### if starttime&endtime are provided, use them
    if 'starttime' in request_GET and 'endtime' in request_GET:
        nhours = -1
        ### starttime
        starttime = request_GET['starttime']
        try:
            dt_start = datetime.strptime(starttime, defaultDatetimeFormat)
        except ValueError:
            errors_GET['starttime'] = \
                'Provided starttime [%s] has incorrect format, expected [%s].' % \
                (starttime, defaultDatetimeFormat)
            starttime = datetime.utcnow() - timedelta(hours=nhours)
            starttime = starttime.replace(tzinfo=pytz.utc).strftime(defaultDatetimeFormat)
        ### endtime
        endtime = request_GET['endtime']
        try:
            dt_end = datetime.strptime(endtime, defaultDatetimeFormat)
        except ValueError:
            errors_GET['endtime'] = \
                'Provided endtime [%s] has incorrect format, expected [%s].' % \
                (endtime, defaultDatetimeFormat)
            endtime = datetime.utcnow()
            endtime = endtime.replace(tzinfo=pytz.utc).strftime(defaultDatetimeFormat)
    ### if nhours is provided, do query "last N days"
    elif 'nhours' in request_GET:
        try:
            nhours = int(request_GET['nhours'])
        except:
            nhours = 12
            errors_GET['nhours'] = \
                'Wrong or no nhours has been provided.Using [%s].' % \
                (nhours)
        starttime = datetime.utcnow() - timedelta(hours=nhours)
        starttime = starttime.replace(tzinfo=pytz.utc).strftime(defaultDatetimeFormat)
        endtime = datetime.utcnow()
        endtime = endtime.replace(tzinfo=pytz.utc).strftime(defaultDatetimeFormat)
    ### neither nhours, nor starttime&endtime was provided
    else:
        nhours = 12
        starttime = datetime.utcnow() - timedelta(hours=nhours)
        starttime = starttime.replace(tzinfo=pytz.utc).strftime(defaultDatetimeFormat)
        endtime = datetime.utcnow()
        endtime = endtime.replace(tzinfo=pytz.utc).strftime(defaultDatetimeFormat)
        errors_GET['noparams'] = \
                'Neither nhours, nor starttime & endtime has been provided. Using starttime=%s and endtime=%s.' % \
                (starttime, endtime)

    ### if mcp_cloud is provided, use it. comma delimited strings
    f_mcp_cloud = ''
    if 'mcp_cloud' in request_GET:
        f_mcp_cloud = request_GET['mcp_cloud']

    ### if computingsite is provided, use it. comma delimited strings
    f_computingsite = ''
    if 'computingsite' in request_GET:
        f_computingsite = request_GET['computingsite']

    ### if jobstatus is provided, use it. comma delimited strings
    f_jobstatus = ''
    if 'jobstatus' in request_GET:
        f_jobstatus = request_GET['jobstatus']

    ### if jobstatus is provided, use it. comma delimited strings
    f_corecount = ''
    if 'corecount' in request_GET:
        f_corecount = request_GET['corecount']

    return starttime, endtime, nhours, errors_GET, \
        f_computingsite, f_mcp_cloud, f_jobstatus, f_corecount


def get_topo_info():
    res = {}
    schedinfo = Schedconfig.objects.all().values('cloud', 'siteid', 'gstat', 'site', 'corecount')
    res = dict([(x['siteid'], x) for x in schedinfo])
    return res


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
    return res


def summarize_data(data, query):
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
    ### get all sites topo from schedconfig table
    schedinfo = get_topo_info()
    ### get list of computing sites
    computingsites = list(set([x['computingsite'] for x in data]))
    ### loop through computing sites, sum njobs for each job status
    for computingsite in computingsites:
        item={'computingsite': computingsite}
        ### add topology info
        cloud = None
        atlas_site = None
        corecount = None
        if computingsite in schedinfo:
            cs_schedinfo = schedinfo[computingsite]
            cloud = cs_schedinfo['cloud']
            atlas_site = cs_schedinfo['gstat']
            corecount = cs_schedinfo['corecount']
        item['cloud'] = cloud
        item['atlas_site'] = atlas_site
        item['corecount'] = corecount
        ### get records for this computingsite
        rec = [x for x in data \
               if x['computingsite'] == computingsite]
        ### get cloud for this computingsite
        mcp_cloud = ','.join(sorted(list(set([x['cloud'] for x in data \
                 if x['computingsite'] == computingsite and len(x['cloud']) > 1]))))
        item['mcp_cloud'] = mcp_cloud
        ### get njobs per jobstatus for this computingsite
        for jobstatus in STATELIST:
            process_jobstatus = False
            if 'jobstatus__in' in query.keys() and jobstatus in query['jobstatus__in']:
                process_jobstatus = True
            elif 'jobstatus__in' not in query.keys():
                process_jobstatus = True
            if process_jobstatus:
                jobstatus_rec = [x['njobs'] for x in rec \
                             if x['jobstatus'] == jobstatus]
                item[jobstatus] = sum(jobstatus_rec)
            else:
                item[jobstatus] = None
        ### store info for this computingsite
        result.append(item)
    ### sort result
    result = sort_data_by_cloud(result)
    return result




