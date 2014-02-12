""" 
htcondor.views

"""

import json
import logging
import pytz
import re
from datetime import datetime, timedelta
from dateutil import parser
from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import ensure_csrf_cookie
from django_datatables_view.base_datatable_view import BaseDatatableView
from ..settings import STATIC_URL, FILTER_UI_ENV
from ..core.utils import getPrefix, getContextVariables, \
        getAoColumnsDictWithTitles
from ..htcondor.models import HTCondorJob
from ..api.htcondorapi.serializers import SerializerHTCondorJob
from ..core.datatablesviews import ModelJobDictJson  # as HTCondorJobDictJson

_logger = logging.getLogger(__name__)

currentDateFormat = "%Y-%m-%d %H:%M:%SZ"
currentDateFormatPost = "%Y-%m-%dT%H:%M:%SZ"
VALUE_TRANSLATION = { \
    'lt': '<', \
    'gt': '>', \
}
WILDCARDS = FILTER_UI_ENV['WILDCARDS']
INTERVALWILDCARDS = FILTER_UI_ENV['INTERVALWILDCARDS']
LAST_N_DAYS = FILTER_UI_ENV['DAYS']

def htcondorJobDetails(request, globaljobid):
    jobs = []
    job = {}
    jobs.extend(HTCondorJob.objects.filter(globaljobid=globaljobid).values())
    if len(jobs):
        try:
            job = jobs[0]
        except IndexError:
            job = {}
    jobInfo = []
    jobKeys = job.keys()

    for key in sorted(jobKeys):
        jobInfo.append((key, str(job[key])))
    _logger.debug('jobInfo=' + str(jobInfo))
    name = ''
    if 'globaljobid' in jobKeys:
        name = job['globaljobid']
    if request.META.get('CONTENT_TYPE', 'text/plain') == 'text/plain':
        data = {
            'prefix': getPrefix(request),
            'jobInfo': jobInfo, 'name': name,
        }
        data.update(getContextVariables(request))
        return render_to_response('htcondor/details_job.html', data, RequestContext(request))
    elif request.META.get('CONTENT_TYPE', 'text/plain') == 'application/json':
        return  HttpResponse(json_dumps(jobInfo), mimetype='text/html')


@ensure_csrf_cookie
def list3HTCondorJobs(request):
    ### get URL prefix
    prefix = getPrefix(request)
    ### get reverse url of the data view
    dataUrl = reverse('api-datatables-htcondor-jobs')
    ### get aoColumns pre-config
    aoColumns = [FILTER_UI_ENV['EXPAND_BUTTON']]
    aoColumns += getAoColumnsDictWithTitles(HTCondorJob._meta.columnTitles)

    data = { \
            'prefix': prefix, \
            'datasrc': str(dataUrl + "?format=json"), \
            'columns': json.dumps(aoColumns), \
    }
    data.update(getContextVariables(request))
    return render_to_response('htcondor/list3.html', data, RequestContext(request))


class HTCondorJobDictJson(ModelJobDictJson):
    model = HTCondorJob
