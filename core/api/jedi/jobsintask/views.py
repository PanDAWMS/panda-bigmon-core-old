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
###DEBUG###    startdate = datetime.utcnow() - timedelta(hours=LAST_N_HOURS)
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
                            jeditaskid=4000195
                        ,
                    ), \
            )
        return qs


    def get_context_data(self, *args, **kwargs):
        return super(PandaJobDictJsonJobsInTask, self).get_context_data(*args, **kwargs)


    def filter_queryset(self, qs):
        qs = QuerySetChain(\
                    Jobsactive4.objects.filter(\
                            jeditaskid=4000195
                        ,
                    ), \
            )
        return qs

#    def filter_queryset(self, qs):
#        # use request parameters to filter queryset
#        ### get the POST keys
#        POSTkeys = self.request.POST.keys()
#        ### see if we filtered from UI
#        pgst = ''
#        if 'pgst' in POSTkeys:
#            pgst = self.request.POST['pgst']
#        if pgst == 'ini':
#            return qs
#        ### assemble query from POST parameters for the filter
#        query = {}
#        for filterField in PandaJob._meta.filterFields:
#            fName = filterField['name']
#            if fName in POSTkeys:
#                fValue = self.request.POST[fName]
#                fField = filterField['field']
#                fFilterField = filterField['filterField']
#                fType = filterField['type']
#                if fType == 'datetime':
#                    try:
#                        fValue = re.sub(' ', 'T', fValue) + ':00Z'
#                        fValue = datetime.strptime(fValue, currentDateFormatPost).replace(tzinfo=pytz.UTC)
#                    except ValueError:
#                        ### unknown datetime format
#                        _logger.error('Unknown datetime format for filter ' + \
#                                'field [%s] with value [%s].' % (fName, fValue))
#                    query.update({'%s' % (fFilterField) : fValue})
#                else:
#                    query.update({'%s' % (fFilterField) : fValue})
#        ### cleanup for datetime ranges
#        ### .creationtime
#        if 'fCrFrom' in POSTkeys or 'fCrTo' in POSTkeys:
#            ### interval start
#            if 'creationtime__gte' in query.keys():
#                submitted_from = query['creationtime__gte']
#                del query['creationtime__gte']
#            else:
##                creationtime_from = datetime.utcnow() - timedelta(days=1)
#                creationtime_from = datetime(2013, 11, 1, 10, 10, tzinfo=pytz.utc)
#            ### interval end
#            if 'creationtime__lte' in query.keys():
#                creationtime_to = query['creationtime__lte']
#                del query['creationtime__lte']
#            else:
##                creationtime_to = datetime.utcnow()
#                creationtime_to = datetime(2013, 11, 22, 12, 10, tzinfo=pytz.utc)
#            ### range instead
#            query['creationtime__range'] = [creationtime_from, creationtime_to]
#        ### execute filter on the queryset
#        if pgst in ['fltr']:
#            qs = QuerySetChain(\
#                    Jobsdefined4.objects.filter(**query), \
#                    Jobsactive4.objects.filter(**query), \
#                    Jobswaiting4.objects.filter(**query), \
#                    Jobsarchived4.objects.filter(**query) \
#            )
#        return qs

    def filterModel(self, query):
        """
            filterModel
                filter qs or querychain with the query
        """
        return QuerySetChain(\
                    Jobsdefined4.objects.filter(**query), \
                    Jobsactive4.objects.filter(**query), \
                    Jobswaiting4.objects.filter(**query), \
                    Jobsarchived4.objects.filter(**query) \
            )


