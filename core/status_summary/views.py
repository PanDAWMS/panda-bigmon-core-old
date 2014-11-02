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


def index(request):
    """
        index -- status_summary's default page
        
        :param request: Django's HTTP request 
        :type request: django.http.HttpRequest
        
    """
    ### configure time interval for queries
    startdate, enddate, nhours, errors_GET = configure(request.GET)

    ### start the query parameters
    query = {}
    ### filter logdate__range
    query['modificationtime__range'] = [startdate, enddate]

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

    qs_tidy = summarize_data(qs)

    ### set request response data
    data = { \
        'errors_GET': errors_GET,
        'startdate': startdate,
        'enddate': enddate,
        'nhours': nhours,
        'viewParams': {'MON_VO': 'ATLAS'},
        'data': qs_tidy,
    }
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
#    startdate = None
#    enddate = None
#    if 'nhours' in request.GET:
#        try:
#            nhours = int(request.GET['nhours'])
#        except:
#            nhours = 6
#        starttime = (datetime.utcnow() - timedelta(hours=nhours)).strftime(collectorTimeFormat)
#        endtime = datetime.utcnow().strftime(collectorTimeFormat)
#        startdate = starttime
#        enddate = endtime
#    else:
#        if 'starttime' in request.GET:
#            try:
#                starttime = datetime.strptime(request.GET['starttime'], collectorDatetimeFormat).strftime(collectorTimeFormat)
#                startdate = starttime
#            except:
#                starttime = (datetime.utcnow() - timedelta(hours=nhours)).strftime(collectorTimeFormat)
#                startdate = starttime
#        else:
#            starttime = (datetime.utcnow() - timedelta(hours=nhours)).strftime(collectorTimeFormat)
#            startdate = starttime
#
#        if 'endtime' in request.GET:
#            try:
#                endtime = datetime.strptime(request.GET['endtime'], collectorDatetimeFormat).strftime(collectorTimeFormat)
#                enddate = endtime
#            except:
#                endtime = datetime.utcnow().strftime(collectorTimeFormat)
#                enddate = endtime
#        else:
#            endtime = datetime.utcnow().strftime(collectorTimeFormat)
#            enddate = endtime
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
#    query['bintime__range'] = [startdate, enddate]
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
##        return render_to_response('pbm/api_pbm_collector.html', {'data': data}, RequestContext(request))
#        return  HttpResponse(json.dumps(data), mimetype='application/json')
#    elif 'type' not in request.GET.keys() or logtype == None:
##        t = get_template('pbm/api_pbm_collector.html')
##        context = RequestContext(request, {'data':data})
##        return HttpResponse(t.render(context), status=400)
#        return  HttpResponse(json.dumps(data), mimetype='application/json', status=400)
#    elif not len(log_records):
##        t = get_template('pbm/api_pbm_collector.html')
##        context = RequestContext(request, {'data':data})
##        return HttpResponse(t.render(context), status=404)
#        return  HttpResponse(json.dumps(data), mimetype='application/json', status=404)
#    else:
##        t = get_template('pbm/api_pbm_collector.html')
##        context = RequestContext(request, {'data':data})
##        return HttpResponse(t.render(context), status=400)
#        return  HttpResponse(json.dumps(data), mimetype='application/json', status=400)
#
#


