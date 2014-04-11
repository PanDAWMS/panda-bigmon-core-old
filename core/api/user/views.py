""" 
api.user.views

"""
#import inspect

import sys
import traceback
import json
import logging
import commands
import itertools
from datetime import datetime, timedelta
from django.db.models import Count
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework.views import APIView
from ...pandajob.models import PandaJob, Jobsactive4, Jobsdefined4, \
    Jobswaiting4, Jobsarchived4
from ...common.utils import QuerySetChain, subDict, getFilterFieldRenderText, \
    getFilterNameForField
#from .serializers import SerializerPandaJob
from ..jedi.jobsintask.views import PandaJobDictJsonJobsInTask
from ..jedi.jobsintask.serializers import SerializerPandaJob

#### BEGIN: for debug purposes only
#from ....htcondor.models import HTCondorJob
#from .serializers import SerializerHTCondorJob
#from .utils import isSecure, getDN, getFQAN, getRemoteHost, checkBanUser
#import status as htcondorapi_status
#### END: for debug purposes only


from ...table.views import ModelJobDictJson, VALUE_ALL_MULTISTRING
#from ..common.settings import STATIC_URL, FILTER_UI_ENV, defaultDatetimeFormat
from ...common.settings import FILTER_UI_ENV, defaultDatetimeFormat
from ...pandajob.columns_config import COLUMNS, ORDER_COLUMNS, \
    COL_TITLES, SMRYCOL_TITLES, FILTERS, SUMMARY_FIELDS
LAST_N_DAYS = FILTER_UI_ENV['DAYS']
LAST_N_HOURS = FILTER_UI_ENV['HOURS']
LAST_N_DAYS_MAX = FILTER_UI_ENV['MAXDAYS']


#_logger = logging.getLogger(__name__)
_logger = logging.getLogger('user_views')
_django_logger = logging.getLogger('django')

#currentDateFormat = "%Y-%m-%d %H:%M:%SZ"
currentDateFormat = defaultDatetimeFormat
shortUIDateFormat = "%m-%d %H:%M"


class ListActiveUsersDictJson(PandaJobDictJsonJobsInTask):
    """
        PandaJobDictJsonJobsInTask
            reverse url: api-datatables-user-list-active-users
    """
    # The model we're going to show
    model = PandaJob

    # reverse URL
    reverseUrl = 'api-datatables-user-list-active-users'

    # Define subset of columns to be used in this resource
    # define the columns that will be returned
#    columns = PandaJob._meta.allColumns
    columns = COLUMNS[reverseUrl]
    filterFields = FILTERS[reverseUrl]
    onlyColumns = list(set(COLUMNS[reverseUrl] + SUMMARY_FIELDS[reverseUrl]))
    summaryColumns = SUMMARY_FIELDS[reverseUrl]

    # define column names that will be used in sorting
    # order is important and should be same as order of columns
    # displayed by datatables. For non sortable columns use empty
    # value like ''
#    order_columns = PandaJob._meta.orderColumns
    order_columns = ORDER_COLUMNS[reverseUrl]

    # set max limit of records returned, this is used to protect our site if someone tries to attack our site
    # and make it return huge amount of data
    max_display_length = 2000


    def skimData(self, data, columns):
        newData = []
        for item in data:
            try:
                newItem = subDict(item, self.columns)
                newData.append(newItem)
            except:
                pass
        return newData


    def dataDictToList(self, data, orderColumns):
        newData = []
        for item in data:
            newItem = []
            for col in orderColumns:
                value = ""
                try:
                    value = item[col]
                except:
                    pass
                newItem.append(value)
            newData.append(newItem)
        return newData


    def skimDataAndRemoveNones(self, data, orderColumns):
        """
            skimDataAndRemoveNones -- clean up output data of the prepare_results
            
            :param data: serialized queryset data
            :type data: list of dictionaries
            :param orderColumns: list of columns in the job UI table and its summary
            :type orderColumns: list of strings
            
        """
        col = orderColumns[0]
        newData = list(set([x[col] for x in data \
                            if x[col] is not None]))
        newData = [{col: x} for x in sorted(newData)]
        return newData


    def prepare_results(self, qs):
        """
            prepare_results super's prepare_results to get list of dicts instead of list of lists
            args:
                qs ... queryset of the model instances
            return:
                list of dicts with data of the qs items
        
        """
        ### original prepare_results provides data as list of lists
        ### overridden prepare_results, with data as list of dicts
        _logger.debug('mark')
        serializer = SerializerPandaJob(qs, many=True, fields=self.columns)
        _logger.debug('mark')
        data = serializer.data
        _logger.debug('mark')
        newData = self.skimDataAndRemoveNones(data, self.columns)
#        _django_logger.debug('prepare_results: after cleanup')
#        _django_logger.debug('data=' + str(newData[:-1]))
        _logger.debug('mark')
##        _logger.debug('data=' + str(newData))
#        return data
        return newData


    def get_initial_queryset(self):
        """
            get_initial_queryset: override this because PanDA job 
                                  is described by 4 different models
        
        """
        _logger.debug('get_initial_queryset')
#        ### limit modificationtime range
#        startdate = datetime.utcnow() - timedelta(days=3 * LAST_N_DAYS)
#        startdate = startdate.strftime(defaultDatetimeFormat)
#        enddate = datetime.utcnow().strftime(defaultDatetimeFormat)
#        ### get the initial queryset properties
#        query = {\
##            'modificationtime__range': [startdate, enddate], \
##            'jeditaskid__isnull': False \
#        }
        ### get the initial queryset
        qs = QuerySetChain(\
            Jobsdefined4.objects.values(*self.onlyColumns).only(*self.onlyColumns).distinct(), \
            Jobsactive4.objects.values(*self.onlyColumns).only(*self.onlyColumns).distinct(), \
            Jobswaiting4.objects.values(*self.onlyColumns).only(*self.onlyColumns).distinct(), \
            Jobsarchived4.objects.values(*self.onlyColumns).only(*self.onlyColumns).distinct() \
        )
        ### return the initial queryset
        return qs


    def filter_queryset(self, qs):
        return self.get_initial_queryset()


    def pagingData(self, qs_data):
        """ 
            Paging data
        """
        limit = min(int(self.request.REQUEST.get('iDisplayLength', 500)), self.max_display_length)
        # if pagination is disabled ("bPaginate": false)
        if limit == -1:
#            _logger.debug('limit==-1')
            return qs_data
        start = int(self.request.REQUEST.get('iDisplayStart', 0))
        offset = start + limit
#        _logger.debug('limit>-1, start=' + str(start) + ' offset=' + str(offset))
        return qs_data[start:offset]


    def get_context_data(self, smry=0, *args, **kwargs):
        """
            get_context_data
                list of active users has no filtering
                --> total_records == total_display records == 
                        == len(self.prepare_results(self.get_initial_queryset()))
        """
        ret = {}
        ### get original dict for datatables
        request = self.request
        self.initialize(*args, **kwargs)

        ### get initial queryset, contains duplicit active user names
        qs = self.get_initial_queryset()

        ### order initial queryset
        qs = self.ordering(qs)

        ### get unique list of active user names
        qs_data = self.prepare_results(qs)

        ### number of records before paging data
        total_records = len(qs_data)

        ### paging the data
        qs_data = self.pagingData(qs_data)

        # number of records after filtering
        total_display_records = len(qs_data)

        # prepare output data
        aaData = qs_data

        _logger.debug('get_context_data')

        ret = {'sEcho': int(request.REQUEST.get('sEcho', 0)),
               'iTotalRecords': total_records,
               'iTotalDisplayRecords': total_display_records,
               'aaData': aaData
               }

        ### correct for wrong/too small iTotalRecords from the default queryset
        try:
            if ret['iTotalRecords'] < ret['iTotalDisplayRecords']:
                ret['iTotalRecords'] = ret['iTotalDisplayRecords']
        except:
            _logger.error('Failed to change iTotalRecords(%s) to iTotalDisplayRecords(%s)'\
                          % (ret['iTotalRecords'], ret['iTotalDisplayRecords']))
        return ret


