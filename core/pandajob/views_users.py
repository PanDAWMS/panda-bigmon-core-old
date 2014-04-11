""" 
views_user

"""

import itertools
from json import dumps as json_dumps
import logging
import pytz
import re
from datetime import datetime, timedelta
from urlparse import parse_qs, urlparse
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import ensure_csrf_cookie
#from django.views.decorators.csrf import csrf_exempt
from django_datatables_view.base_datatable_view import BaseDatatableView
#from ..settings import CUSTOM_DB_FIELDS, FILTER_UI_ENV
from ..common.settings import STATIC_URL, FILTER_UI_ENV, defaultDatetimeFormat
from .models import PandaJob, Jobsactive4, Jobsdefined4, Jobswaiting4, Jobsarchived4
from .serializers import SerializerPandaJob
#from .utils import getPrefix, getContextVariables, \
#        getAoColumnsDictWithTitles, QuerySetChain, subDictToStr
from ..common.utils import getPrefix, getContextVariables, \
        getAoColumnsDictWithTitles, QuerySetChain, subDictToStr, \
        getFilterFieldIDs
#from .datatablesviews import ModelJobDictJson
from ..table.views import ModelJobDictJson
from rest_framework import viewsets
LAST_N_DAYS = FILTER_UI_ENV['DAYS']
LAST_N_HOURS = FILTER_UI_ENV['HOURS']
LAST_N_DAYS_MAX = FILTER_UI_ENV['MAXDAYS']
from .columns_config import COLUMNS, ORDER_COLUMNS, COL_TITLES, FILTERS


#from django.views.decorators.cache import cache_page


#_logger = logging.getLogger(__name__)
_logger = logging.getLogger('bigpandamon')

#currentDateFormat = "%Y-%m-%d %H:%M:%SZ"
currentDateFormat = defaultDatetimeFormat
WILDCARDS = FILTER_UI_ENV['WILDCARDS']
INTERVALWILDCARDS = FILTER_UI_ENV['INTERVALWILDCARDS']
LAST_N_DAYS = FILTER_UI_ENV['DAYS']
LAST_N_HOURS = FILTER_UI_ENV['HOURS']



@ensure_csrf_cookie
def listActiveUsers(request):
    """
        listActiveUsers -- view list of PanDA jobs in a dataTables table
                            data from API jedi/userjobset
        
        :param request: Django's HTTP request 
        :type request: django.http.HttpRequest
        
    """
    reverseUrl = 'api-datatables-user-list-active-users'
    ### get URL prefix
    prefix = getPrefix(request)
    ### get aoColumns pre-config
    aoColumns = []
    aoColumns += getAoColumnsDictWithTitles(COL_TITLES[reverseUrl])
    ### get filter fields
    filterFields = getFilterFieldIDs(FILTERS[reverseUrl])
    ### get indices of columns to refer by name in render javascript function
    fieldIndices = {}
    for col in ORDER_COLUMNS[reverseUrl]:
        i = None
        try:
            i = ORDER_COLUMNS[reverseUrl].index(col)
        except:
            pass
        fieldIndices[col] = i
    ### get reverse url of the data view
    dataUrl = reverse(reverseUrl)
    ### set request response data
    data = { \
            'prefix': prefix, \
            'datasrc': str(dataUrl + "?format=json"), \
            'columns': json_dumps(aoColumns), \
            'tableid': 'listactiveusers', \
            'caption': 'users', \
            'fieldIndices': json_dumps(fieldIndices), \
            'filterFields': filterFields, \
    }
    data.update(getContextVariables(request))
    return render_to_response('pandajob/users/listusers.html', data, RequestContext(request))


@ensure_csrf_cookie
def userActivity(request, produsername=''):
    """
        userActivity -- view list of PanDA jobs in a dataTables table
                            data from API jedi/userjobset
        
        :param request: Django's HTTP request 
        :type request: django.http.HttpRequest
        
    """
    reverseUrl = 'api-datatables-user-list-user-activity'
    ### get URL prefix
    prefix = getPrefix(request)
    ### get aoColumns pre-config
    aoColumns = []
    aoColumns += getAoColumnsDictWithTitles(COL_TITLES[reverseUrl])
    ### get filter fields
    filterFields = getFilterFieldIDs(FILTERS[reverseUrl])
    ### get indices of columns to refer by name in render javascript function
    fieldIndices = {}
    for col in ORDER_COLUMNS[reverseUrl]:
        i = None
        try:
            i = ORDER_COLUMNS[reverseUrl].index(col)
        except:
            pass
        fieldIndices[col] = i
    ### get reverse url of the data view
    dataUrl = reverse(reverseUrl)
    ### set request response data
    data = { \
            'prefix': prefix, \
            'datasrc': str(dataUrl + "?format=json"), \
            'columns': json_dumps(aoColumns), \
            'tableid': 'useractivity', \
            'caption': produsername, \
            'fieldIndices': json_dumps(fieldIndices), \
            'filterFields': filterFields, \
    }
    data.update(getContextVariables(request))
    return render_to_response('pandajob/users/useractivity.html', data, RequestContext(request))


