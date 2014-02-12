""" 
views

"""

import itertools
from json import dumps as json_dumps
import logging
import pytz
import re
from datetime import datetime, timedelta
from urlparse import parse_qs, urlparse
from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import ensure_csrf_cookie
#from django.views.decorators.csrf import csrf_exempt
from django_datatables_view.base_datatable_view import BaseDatatableView
#from ..settings import CUSTOM_DB_FIELDS, FILTER_UI_ENV
from settings import CUSTOM_DB_FIELDS, FILTER_UI_ENV
#from .models import PandaJob, Jobsactive4, Jobsdefined4, Jobswaiting4, Jobsarchived4
from ..pandajob.models import PandaJob, Jobsactive4, Jobsdefined4, Jobswaiting4, Jobsarchived4
#from .serializers import SerializerPandaJob
from ..pandajob.serializers import SerializerPandaJob
from .utils import getPrefix, getContextVariables, \
        getAoColumnsDictWithTitles, QuerySetChain, subDictToStr
#from .datatablesviews import ModelJobDictJson
from ..table.views import ModelJobDictJson
from rest_framework import viewsets

_logger = logging.getLogger(__name__)

currentDateFormat = "%Y-%m-%d %H:%M:%SZ"
WILDCARDS = FILTER_UI_ENV['WILDCARDS']
INTERVALWILDCARDS = FILTER_UI_ENV['INTERVALWILDCARDS']
LAST_N_DAYS = FILTER_UI_ENV['DAYS']

# Create your views here.
def index(request):
    """
    Index page view
    
    """
    data = {}
    data.update(getContextVariables(request))
#    return render_to_response('core/_index_grid.html', data, RequestContext(request))
    return render_to_response('_index_grid.html', data, RequestContext(request))


def graceful404(request):
    """
    graceful404 -- return our 404.html even if settings.DEBUG=True.
    
    """
    return render_to_response('404.html', {}, RequestContext(request))


def testing(request):
    """
    testing view
    
    """
    data = {}
    data.update(getContextVariables(request))
    return render_to_response('core/testing.html', data, RequestContext(request))


