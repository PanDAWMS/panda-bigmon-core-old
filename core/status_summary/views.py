""" 
core.status_summary.views

"""

import logging
import json
import pytz
from datetime import datetime, timedelta

from django.db.models import Count, Sum
from django.shortcuts import render_to_response, render
from django.template import RequestContext, loader
from django.http import HttpResponse
from django.template.loader import get_template
from django.core.serializers.json import DjangoJSONEncoder

from .utils import configure, summarize_data

from ..pandajob.models import Jobsactive4, Jobsdefined4, Jobswaiting4, \
    Jobsarchived4


collectorDatetimeFormat = "%Y-%m-%dT%H:%M:%S"
#collectorDateFormat = "%Y-%m-%d"
#collectorDateFormat = collectorDatetimeFormat
collectorTimeFormat = "%Y-%m-%d %H:%M:%S"


_logger = logging.getLogger('bigpandamon')


def index_data(request):
    """
        index -- status_summary's default page
        
        :param request: Django's HTTP request 
        :type request: django.http.HttpRequest
        
        
        filtering options for specified GET parameters:
            ?nhours ... date range of how many hours in past
            ?starttime ... datetime from, format %Y-%m-%dT%H:%M:%S
            ?endtime ... datetime to, format %Y-%m-%dT%H:%M:%S
            ?mcp_cloud ... cloud field of the jobs tables
            ?computingsite ... computingsite field of the jobs tables
            ?jobstatus ... PanDA job status, list delimited by comma
            ?corecount .. corecount field of the schedconfig table
            nhours has higher priority than starttime, endtime
                if nhours is specified, starttime&endtime are not taken into account.
        
    """
    errors = {}
    warnings = {}

    ### GET parameters
    GET_parameters = {}
    for p in request.GET:
        GET_parameters[p] = str(request.GET[p])

    ### time range from request.GET
    optionalFields = ['nhours', 'starttime', 'endtime', \
                      'mcp_cloud', 'computingsite', 'jobstatus', 'corecount']
    for optionalField in optionalFields:
        try:
            if len(request.GET[optionalField]) < 1:
                msg = 'Missing optional GET parameter %s. ' % optionalField
                if 'missingoptionalparameter' not in warnings.keys():
                    warnings['missingoptionalparameter'] = ''
                warnings['missingoptionalparameter'] += msg
        except:
            msg = 'Missing optional GET parameter %s. ' % optionalField
            _logger.warning(msg)
            if 'missingoptionalparameter' not in warnings.keys():
                warnings['missingoptionalparameter'] = ''
            warnings['missingoptionalparameter'] += msg

    ### if all expected GET parameters are present, execute log lookup

    ### configure time interval for queries
    starttime, endtime, nhours, errors_GET, \
        f_computingsite, f_mcp_cloud, f_jobstatus, f_corecount \
 = configure(GET_parameters)

    ### start the query parameters
    query = {}
    ### filter logdate__range
    query['modificationtime__range'] = [starttime, endtime]
    ### filter mcp_cloud
    fval_mcp_cloud = f_mcp_cloud.split(',')
    print 'fval_mcp_cloud', fval_mcp_cloud
    if len(fval_mcp_cloud) and len(fval_mcp_cloud[0]):
        query['cloud__in'] = fval_mcp_cloud
    ### filter computingsite
    fval_computingsite = f_computingsite.split(',')
    if len(fval_computingsite) and len(fval_computingsite[0]):
        query['computingsite__in'] = fval_computingsite
    ### filter jobstatus
    fval_jobstatus = f_jobstatus.split(',')
    if len(fval_jobstatus) and len(fval_jobstatus[0]):
        query['jobstatus__in'] = fval_jobstatus
    ### filter corecount
    fval_corecount = f_corecount.split(',')
    if len(fval_corecount) and len(fval_corecount[0]):
        query['corecount__in'] = fval_corecount

    ### query jobs for the summary
    qs = []
    qs.extend( 
        Jobsactive4.objects.filter(**query).values('jobstatus', 'cloud', 'computingsite' \
        ).annotate(njobs=Count('jobstatus') \
        ).order_by('cloud', 'computingsite', 'jobstatus')
    )
    qs.extend(
        Jobsdefined4.objects.filter(**query).values('jobstatus', 'cloud', 'computingsite' \
        ).annotate(njobs=Count('jobstatus') \
        ).order_by('cloud', 'computingsite', 'jobstatus')
    )
    qs.extend(
        Jobswaiting4.objects.filter(**query).values('jobstatus', 'cloud', 'computingsite' \
        ).annotate(njobs=Count('jobstatus') \
        ).order_by('cloud', 'computingsite', 'jobstatus')
    )
    qs.extend(
        Jobsarchived4.objects.filter(**query).values('jobstatus', 'cloud', 'computingsite' \
        ).annotate(njobs=Count('jobstatus') \
        ).order_by('cloud', 'computingsite', 'jobstatus')
    )

    qs_tidy = summarize_data(qs, query)

    ### set request response data
    data = { \
        'errors_GET': errors_GET,
        'starttime': starttime,
        'endtime': endtime,
        'nhours': nhours,
        'query': query,
        'GETparams': GET_parameters,
        'data': qs_tidy,
    }
    return data, errors, warnings, query, GET_parameters


def api_status_summary(request):
    """
        api_status_summary -- api for status_summary's default page
        
        :param request: Django's HTTP request 
        :type request: django.http.HttpRequest
        
        for filtering options see index_data
    """
    raw_data_dict, errors, warnings, query, GET_parameters = index_data(request)
    raw_data = raw_data_dict['data']
    data = { \
        'timestamp': datetime.utcnow().isoformat(), \
        'errors': errors, \
        'warnings': warnings, \
        'query': query, \
        'GET_parameters': GET_parameters, \
        'nrecords': len(raw_data), \
        'data': raw_data \
    }

    if not len(errors) and len(raw_data):
        ### set request response data
        return  HttpResponse(json.dumps(data), mimetype='application/json')
    elif not len(raw_data):
        return  HttpResponse(json.dumps(data), mimetype='application/json', status=404)
    else:
        return  HttpResponse(json.dumps(data), mimetype='application/json', status=400)


def index(request):
    """
        index -- status_summary's default page
        
        :param request: Django's HTTP request 
        :type request: django.http.HttpRequest
        
        for filtering options see index_data
    """
    ### if curling for json, return API response
    if request.META.get('CONTENT_TYPE', 'text/plain') == 'application/json':
        return api_status_summary(request)

    data, errors, warnings, query, GET_parameters = index_data(request)
    data['viewParams'] = {'MON_VO': 'ATLAS'},
    return render_to_response('status_summary/index-status_summary.html', data, RequestContext(request))


