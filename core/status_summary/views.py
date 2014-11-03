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
                      'mcp_cloud', 'computingsite', 'jobstatus']
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
        f_computingsite, f_mcp_cloud, f_jobstatus = configure(GET_parameters)

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


#def api_pbm_collector(request):
#    """
#        api_pbm_collector -- return json with Pandalog data for specified GET parameters
#            ?type ... Pandalog flavour, e.g. 'pd2p', 'brokerage', 'analy_brokerage'
#            ?nhours ... date range of how many hours in past
#            ?starttime ... datetime from, format %Y-%m-%dT%H:%M:%S
#            ?endtime ... datetime to, format %Y-%m-%dT%H:%M:%S
#
#            nhours has higher priority than starttime, endtime
#                if nhours is specified, starttime&endtime are not taken into account.
#
#        :param request: Django's HTTP request
#        :type request: django.http.HttpRequest
#
#    """
#    errors = {}
#    warnings = {}
#
#    ### GET parameters
#    GET_parameters = {}
#    for p in request.GET:
#        GET_parameters[p] = str(request.GET[p])
#
#    ### check that all expected parameters are in URL
#    expectedFields = ['type']
#    for expectedField in expectedFields:
#        try:
#            if len(request.GET[expectedField]) < 1:
#                msg = 'Missing expected GET parameter %s. ' % expectedField
#                if 'missingparameter' not in errors.keys():
#                    errors['missingparameter'] = ''
#                errors['missingparameter'] += msg
#        except:
#            msg = 'Missing expected GET parameter %s. ' % expectedField
#            _logger.error(msg)
#            if 'missingparameter' not in errors.keys():
#                errors['missingparameter'] = ''
#            errors['missingparameter'] += msg
#
#    ### time range from request.GET
#    optionalFields = ['starttime', 'endtime', 'nhours']
#    for optionalField in optionalFields:
#        try:
#            if len(request.GET[optionalField]) < 1:
#                msg = 'Missing optional GET parameter %s. ' % optionalField
#                if 'missingoptionalparameter' not in warnings.keys():
#                    warnings['missingoptionalparameter'] = ''
#                warnings['missingoptionalparameter'] += msg
#        except:
#            msg = 'Missing optional GET parameter %s. ' % optionalField
#            _logger.warning(msg)
#            if 'missingoptionalparameter' not in warnings.keys():
#                warnings['missingoptionalparameter'] = ''
#            warnings['missingoptionalparameter'] += msg
#    ### get values for optional timerange parameters
#    nhours = 6
#    starttime = None
#    endtime = None
#    starttime = None
#    endtime = None
#    if 'nhours' in request.GET:
#        try:
#            nhours = int(request.GET['nhours'])
#        except:
#            nhours = 6
#        starttime = (datetime.utcnow() - timedelta(hours=nhours)).strftime(collectorTimeFormat)
#        endtime = datetime.utcnow().strftime(collectorTimeFormat)
#        starttime = starttime
#        endtime = endtime
#    else:
#        if 'starttime' in request.GET:
#            try:
#                starttime = datetime.strptime(request.GET['starttime'], collectorDatetimeFormat).strftime(collectorTimeFormat)
#                starttime = starttime
#            except:
#                starttime = (datetime.utcnow() - timedelta(hours=nhours)).strftime(collectorTimeFormat)
#                starttime = starttime
#        else:
#            starttime = (datetime.utcnow() - timedelta(hours=nhours)).strftime(collectorTimeFormat)
#            starttime = starttime
#
#        if 'endtime' in request.GET:
#            try:
#                endtime = datetime.strptime(request.GET['endtime'], collectorDatetimeFormat).strftime(collectorTimeFormat)
#                endtime = endtime
#            except:
#                endtime = datetime.utcnow().strftime(collectorTimeFormat)
#                endtime = endtime
#        else:
#            endtime = datetime.utcnow().strftime(collectorTimeFormat)
#            endtime = endtime
#
#    ### if all expected GET parameters are present, execute log lookup
#    query = {}
#    logtype = None
#    try:
#        if 'type' in request.GET and len(request.GET['type']):
#            logtype = request.GET['type']
#    except:
#        logtype = None
#    query['type'] = logtype
#    query['bintime__range'] = [starttime, endtime]
#    query['time__range'] = [starttime, endtime]
#
#    log_records = []
#    try:
#        log_records = Pandalog.objects.filter(**query).values()
#    except:
#        pass
#
#    frm_log_records = []
#    if not len(log_records):
#        if 'lookup' not in errors:
#            errors['lookup'] = ''
#        errors['lookup'] += 'Log record for parameters has not been found. query=%s' % query
#    ### return the json data
#    else:
#        frm_log_records = [ {'name': x['name'], \
#                             'bintime': x['bintime'].isoformat(), \
#                             'module': x['module'], \
#                             'loguser': x['loguser'], \
#                             'type': x['type'], \
#                             'pid': x['pid'], \
#                             'loglevel': x['loglevel'], \
#                             'levelname': x['levelname'], \
#                             'filename': x['filename'], \
#                             'line': x['line'], \
#                             'time': x['time'], \
#                             'message': x['message'] \
#                             } \
#                           for x in log_records ]
#
#    data = { \
#        'timestamp': datetime.utcnow().isoformat(), \
#        'errors': errors, \
#        'warnings': warnings, \
#        'query': query, \
#        'GET_parameters': GET_parameters, \
#        'nrecords': len(log_records), \
#        'data': frm_log_records \
#    }
#    if not len(errors):
#        ### set request response data
#        return  HttpResponse(json.dumps(data), mimetype='application/json')
#    elif 'type' not in request.GET.keys() or logtype == None:
#        return  HttpResponse(json.dumps(data), mimetype='application/json', status=400)
#    elif not len(log_records):
#        return  HttpResponse(json.dumps(data), mimetype='application/json', status=404)
#    else:
#        return  HttpResponse(json.dumps(data), mimetype='application/json', status=400)
#
#


