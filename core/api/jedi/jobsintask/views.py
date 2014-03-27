""" 
api.jedi.jobsintask.views

"""
import sys
import json
import logging
import commands
import itertools
from datetime import datetime, timedelta
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework.views import APIView
from ....pandajob.models import PandaJob, Jobsactive4, Jobsdefined4, \
    Jobswaiting4, Jobsarchived4
from ....common.utils import QuerySetChain, subDict
from .serializers import SerializerPandaJob

#### BEGIN: for debug purposes only
#from ....htcondor.models import HTCondorJob
#from .serializers import SerializerHTCondorJob
#from .utils import isSecure, getDN, getFQAN, getRemoteHost, checkBanUser
#import status as htcondorapi_status
#### END: for debug purposes only


from ....table.views import ModelJobDictJson
#from ..common.settings import STATIC_URL, FILTER_UI_ENV, defaultDatetimeFormat
from ....common.settings import FILTER_UI_ENV, defaultDatetimeFormat
from ....pandajob.columns_config import COLUMNS, ORDER_COLUMNS, COL_TITLES, FILTERS
LAST_N_DAYS = FILTER_UI_ENV['DAYS']
LAST_N_HOURS = FILTER_UI_ENV['HOURS']
LAST_N_DAYS_MAX = FILTER_UI_ENV['MAXDAYS']


#_logger = logging.getLogger(__name__)
_logger = logging.getLogger('jedi_jobsintask')

currentDateFormat = "%Y-%m-%d %H:%M:%SZ"
shortUIDateFormat = "%m-%d %H:%M"


#class PandaJobsViewSet(viewsets.ModelViewSet):
#    """
#        API resource that allows PanDA jobs listed
#
#    """
#    model = PandaJob
#    serializer_class = SerializerPandaJob
#
#
#    def listJobsInTask(self, request):
#        """
#            list
#            args:
#                request
#            returns:
#                Response with HTTP status code
#                    data/errors
#
#        """
#
#        queryset = list(itertools.chain(HTCondorJob.objects.all()))
#        serializer = SerializerPandaJob(queryset, many=True)
#        return Response(serializer.data)
#
#
#    def listForDataTables(self, request):
#        """
#            listForDataTables
#            args:
#                request
#            returns:
#                Response with HTTP status code
#                    data/errors
#
#        """
#        queryset = list(itertools.chain(HTCondorJob.objects.all()))
#        serializer = SerializerHTCondorJob(queryset, many=True)
#        data = serializer.data[:5]
##        data = serializer.data
#        return Response({"aaData": data, "result": "ok", \
##                         "sEcho": 0, \
#                         "iTotalRecords": len(data), \
#                         "iTotalDisplayRecords": len(data) \
#                    })




class PandaJobDictJsonJobsInTask(ModelJobDictJson):
    """
        PandaJobDictJsonJobsInTask
            reverse url: api-datatables-jedi-jobs-in-task
        
    """
    # The model we're going to show
    model = PandaJob

    # reverse URL
    reverseUrl = 'api-datatables-jedi-jobs-in-task'

    # Define subset of columns to be used in this resource
    # define the columns that will be returned
#    columns = PandaJob._meta.allColumns
    columns = COLUMNS[reverseUrl]
    filterFields = FILTERS[reverseUrl]

    # define column names that will be used in sorting
    # order is important and should be same as order of columns
    # displayed by datatables. For non sortable columns use empty
    # value like ''
#    order_columns = PandaJob._meta.orderColumns
    order_columns = ORDER_COLUMNS[reverseUrl]

    # set max limit of records returned, this is used to protect our site if someone tries to attack our site
    # and make it return huge amount of data
    max_display_length = 500


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


    def removeNones(self, data, orderColumns):
        convertDatetimeToString = False
        POSTkeys = self.request.POST.keys()
        if 'pgst' in POSTkeys:
            convertDatetimeToString = True
        newData = []
        for item in data:
            newItem = {}
            for col in orderColumns:
                value = ""
                try:
                    value = item[col]
                    if value is None:
                        value = ""
                except:
                    pass
                if convertDatetimeToString and \
                    (type(value) == type(datetime(1970, 1, 1)) ):
                    try:
                        _logger.debug('value=' + (str({"k": value})))
                        valueStr = value.strftime(shortUIDateFormat)
                        _logger.debug('valueStr=' + (str({"k": valueStr})))
                        value = valueStr
                    except:
                        pass
                newItem[col] = value
            newData.append(newItem)
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
        _logger.debug('qs=' + str(qs))
        serializer = SerializerPandaJob(qs, many=True)
        _logger.debug('mark')
        data = serializer.data
        newData = self.skimData(data, self.columns)
        newData = self.removeNones(newData, self.columns)
#        newData = self.dataDictToList(newData, self.order_columns)
        _logger.debug('mark')
        _logger.debug('data=' + str(newData))
#        return data
        return newData


    def get_initial_queryset(self):
        """
            get_initial_queryset: override this because PanDA job 
                                  is described by 4 different models
        
        """
###DEBUG###        startdate = datetime.utcnow() - timedelta(hours=LAST_N_HOURS)
###DEBUG###        startdate = datetime.utcnow() - timedelta(days=LAST_N_DAYS)
        startdate = datetime.utcnow() - timedelta(minutes=2)
        startdate = startdate.strftime(defaultDatetimeFormat)
        enddate = datetime.utcnow().strftime(defaultDatetimeFormat)
#        qs = QuerySetChain(\
#                    Jobsdefined4.objects.filter(\
#                        modificationtime__range=[startdate, enddate]\
#                    ), \
#                    Jobsactive4.objects.filter(\
#                        modificationtime__range=[startdate, enddate]\
#                    ), \
#                    Jobswaiting4.objects.filter(\
#                        modificationtime__range=[startdate, enddate]\
#                    ), \
#                    Jobsarchived4.objects.filter(\
#                        modificationtime__range=[startdate, enddate]\
#                    ), \
#            )
        qs = QuerySetChain(\
                    Jobsactive4.objects.filter(\
                            jeditaskid=4000195, \
#                            modificationtime__range=[startdate, enddate], \
                    ), \
            )
        return qs


    def get_context_data(self, *args, **kwargs):
        return super(PandaJobDictJsonJobsInTask, self).get_context_data(*args, **kwargs)


    def filter_querysetOld(self, qs):
        # use request parameters to filter queryset
        ### get the POST keys
        POSTkeys = self.request.POST.keys()
        _logger.debug('POSTkeys=' + str(POSTkeys))
        _logger.debug('POSTvalues=' + str(self.request.POST))
        qs = QuerySetChain(\
                    Jobsactive4.objects.filter(\
                            jeditaskid=4000195, \
#                            modificationtime__range=[startdate, enddate], \
                    ), \
            )
        return qs

    def filter_queryset(self, qs):
        # use request parameters to filter queryset
        ### get the POST keys
        POSTkeys = self.request.POST.keys()
        ### see if we filtered from UI
        pgst = ''
        if 'pgst' in POSTkeys:
            pgst = self.request.POST['pgst']
        if pgst == 'ini':
            return qs
        ### assemble query from POST parameters for the filter
        query = {}
        for filterField in self.filterFields:
            fName = filterField['name']
            if fName in POSTkeys:
                fValue = self.request.POST[fName]
                fField = filterField['field']
                fFilterField = filterField['filterField']
                fType = filterField['type']
                ### process datetime types
                if fType == 'datetime':
                    fValue = self.getQueryValueDatetime(fName, fValue)
                    query.update({'%s' % (fFilterField) : fValue})
                ### process string with multiple selection
                elif fType == 'stringMultiple':
                    val, suffix = self.getQueryValueStringmultiple(fName, fValue)
                    query['%s%s' % (fField, suffix)] = val
                ### process wildcarded strings
                elif fType == 'string':
                    retVal = self.getQueryValueStringWildcard(fValue)
                    for val, suffix in retVal:
                        query['%s%s' % (fField, suffix)] = val
                ### process wildcarded integers
                elif fType == 'integer':
                    retVal = self.getQueryValueIntIntervalWildcard(fValue)
                    for val, suffix in retVal:
                        query['%s%s' % (fField, suffix)] = val
                ### process anything else
                else:
                    query.update({'%s' % (fFilterField) : fValue})
        ### cleanup for datetime ranges
        query = self.cleanupDatetimeRange(POSTkeys, query)
        ### execute filter on the queryset
        if pgst in ['fltr']:
            qs = QuerySetChain(\
#                    Jobsdefined4.objects.filter(**query), \
                    Jobsactive4.objects.filter(**query), \
#                    Jobswaiting4.objects.filter(**query), \
#                    Jobsarchived4.objects.filter(**query) \
            )
            _logger.debug('|qs|=%d' % (qs.count()))
        return qs


    def filterModel(self, query):
        """
            filterModel
                filter qs or querychain with the query
        """
        return QuerySetChain(\
##                    Jobsactive4.objects.filter(\
##                            jeditaskid=4000195, \
##                            modificationtime__range=[startdate, enddate], \
##                    ), \
#                    Jobsdefined4.objects.filter(**query), \
                    Jobsactive4.objects.filter(**query), \
#                    Jobswaiting4.objects.filter(**query), \
#                    Jobsarchived4.objects.filter(**query) \
            )


