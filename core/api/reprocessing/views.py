""" 
api.jedi.jobsintask.views

"""
#import inspect

import sys
import traceback
import inspect
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
    Jobswaiting4, Jobsarchived4, Jobsarchived
from ...common.utils import QuerySetChain, subDict, getFilterFieldRenderText, \
    getFilterNameForField
from ...common.models import JediTasks
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
_logger = logging.getLogger('api_reprocessing')
_django_logger = logging.getLogger('django')

#currentDateFormat = "%Y-%m-%d %H:%M:%SZ"
currentDateFormat = defaultDatetimeFormat
shortUIDateFormat = "%m-%d %H:%M"


class PandaJobDictJsonReprocessingSmryPage(ModelJobDictJson):
    """
        PandaJobDictJsonReprocessingSmryPage
            reverse url: api-reprocessing-jobs-in-task-smry
        
    """
    # The model we're going to show
    model = PandaJob

    # reverse URL
    reverseUrl = 'api-reprocessing-jobs-in-task-smry'

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
#    max_display_length = 2000
    max_display_length = 10000

    queryDict = {}

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


#    def removeNones(self, data, orderColumns):
    def skimDataAndRemoveNones(self, data, orderColumns):
        convertDatetimeToString = False
        POSTkeys = self.request.POST.keys()
        if 'pgst' in POSTkeys:
            convertDatetimeToString = True
        newData = []
        for item in data:
#            newItem = {}
            ### skim data
            newItem = subDict(item, self.columns)
            ### remove None (replace by "")
            ### and format datetime string
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
                        valueStr = value.strftime(shortUIDateFormat)
                        value = valueStr
                    except:
                        pass
                newItem[col] = value
            ### prodsourcelabel, jobsetid handling
            prodsourcelabel = ""
            try:
                prodsourcelabel = item['prodsourcelabel']
            except:
                _logger.error('Could not determine prodsourcelabel for item [%s]' % (str(item)))
            ### handle jobsetid:
            ###    prodsourcelabel != 'user; : set empty jobsetid
            ###    prodsourcelabel == 'user' : keep the jobsetid value
            if prodsourcelabel != 'user':
                newItem['jobsetid'] = ""
            ### delete prodsourcelabel from the result
            try:
                del newItem['prodsourcelabel']
            except:
                _logger.error('Could not delete prodsourcelabel from item [%s]' % (str(item)))
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
#        _logger.debug('prepare_results: caller name:' + str(inspect.stack()[1][3]))
        ### original prepare_results provides data as list of lists
        serializer = SerializerPandaJob(qs, many=True, fields=self.columns)
#        _django_logger.debug('prepare_results: after SerializerPandaJob')
        _logger.debug('mark')
        data = serializer.data
        newData = self.skimDataAndRemoveNones(data, self.columns)
        _logger.debug('mark')
        return newData


    def get_initial_queryset(self):
        """
            get_initial_queryset: override this because PanDA job 
                                  is described by 4 different models
        
        """
        ### limit modificationtime range
#        startdate = datetime.utcnow() - timedelta(days=LAST_N_DAYS)
        startdate = datetime.utcnow() - timedelta(minutes=5)
        startdate = startdate.strftime(defaultDatetimeFormat)
        enddate = datetime.utcnow().strftime(defaultDatetimeFormat)
        ### get the initial queryset properties
        query = {\
            'modificationtime__range': [startdate, enddate]
        }
        ### get the initial queryset
        qs = QuerySetChain(\
            Jobsdefined4.objects.filter(**query).only(*self.onlyColumns), \
            Jobsactive4.objects.filter(**query).only(*self.onlyColumns), \
            Jobswaiting4.objects.filter(**query).only(*self.onlyColumns), \
            Jobsarchived4.objects.filter(**query).only(*self.onlyColumns), \
            Jobsarchived.objects.filter(**query).only(*self.onlyColumns) \
        )
        ### return the initial queryset
        return qs


    def getFilterFromPost(self, requestKeys):
        """
            getFilterFromPost -- prepare query for queryset
        """
        ### assemble query from POST parameters for the filter
        print 'Entered getFilterFromPost'
        query = {}
        for filterField in self.filterFields:
            fName = filterField['name']
            if fName in requestKeys:
                fValue = ''
                if fName in self.request.POST:
                    fValue = self.request.POST[fName]
                elif fName in self.request.GET:
                    fValue = self.request.GET[fName]
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
                    ### val=='all'==VALUE_ALL_MULTISTRING,
                    ### if VALUE_ALL_MULTISTRING is selected among values
                    ###     then do not filter by this fField
                    if val != VALUE_ALL_MULTISTRING:
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
        query = self.cleanupDatetimeRange(requestKeys, query)
        ### return query dict
        return query


    def getFilterForTaskname(self, fName, fValue):
        query = {}
        retVal = self.getQueryValueStringWildcard(fValue)
        for val, suffix in retVal:
            query['%s%s' % (fName, suffix)] = val
        return query


    def filter_queryset(self, qs):
#        _logger.debug('filter_queryset qs: %s' % (str(qs)))
#        _logger.debug('filter_queryset: caller name:' + str(inspect.stack()[1][3]))
        # use request parameters to filter queryset
        ### get the POST keys
        POSTkeys = self.request.POST.keys()
        GETkeys = self.request.GET.keys()
        ### see if we filtered from UI
        ### if pgst in self.request.POST --> filtered from UI
        pgst = 'fltr'
        if 'pgst' in POSTkeys:
            pgst = self.request.POST['pgst']
        elif 'pgst' in GETkeys:
            pgst = self.request.GET['pgst']
        if pgst == 'ini':
#            _logger.debug('|qs|=%d' % (qs.count()))
            return qs
        ### handle the taskname filter: taskname is not a field of Jobs object
        qs_taskname_ids = []
        taskname_query = {}
        taskname_query_val=''
        if 'taskname' in POSTkeys:
            try:
                taskname_query_val = self.request.POST['taskname']
                del self.request.POST['taskname']
            except:
                _logger.error('Cannot remove "taskname" entry from the query: %s' % (str(POSTkeys)))
        elif 'taskname' in GETkeys:
            try:
                taskname_query_val = self.request.GET['taskname']
                del self.request.GET['taskname']
            except:
                _logger.error('Cannot remove "taskname" entry from the query: %s' % (str(GETkeys)))
#        taskname_query_prep = {'taskname': taskname_query_val}
#        taskname_query = self.getFilterFromPost({'taskname': taskname_query_val})
#        taskname_query = self.getFilterFromPost(['taskname'])
#        taskname_query = {'taskname': taskname_query_val}
        taskname_query = self.getFilterForTaskname('taskname', taskname_query_val)
        _logger.debug('taskname_query: %s' % (str(taskname_query)))

        qs_taskname_ids = []
        if taskname_query:
            qs_taskname_ids = JediTasks.objects.filter(**taskname_query).values_list('jeditaskid', flat=True)
        _logger.debug('taskname_query: %s' % (str(taskname_query)))
        _logger.debug('qs_taskname_ids: %s' % (str(qs_taskname_ids)))
        ### assemble query from requests' POST/GET parameters for the filter
        query_post = self.getFilterFromPost(POSTkeys)
        query_get = self.getFilterFromPost(GETkeys)
        query = {}
        query.update(query_post)
        query.update(query_get)
        _logger.debug('query: %s' % (str(query)))
        if len(qs_taskname_ids):
            query['jeditaskid__in'] = qs_taskname_ids
        _logger.debug('query: %s' % (str(query)))
        self.queryDict = {}
        self.queryDict.update(query)
        if taskname_query:
            self.queryDict.update(taskname_query)
        ### execute filter on the queryset
#        _django_logger.debug('filter_queryset: pgst=' + str(pgst))
        if pgst in ['fltr'] and query != {}:
            ### add constraint that jeditaskid is not NULL
            _django_logger.debug('filter_queryset: before filtered qs')
            qs = QuerySetChain(\
                    Jobsdefined4.objects.filter(**query).only(*self.onlyColumns), \
                    Jobsactive4.objects.filter(**query).only(*self.onlyColumns), \
                    Jobswaiting4.objects.filter(**query).only(*self.onlyColumns), \
                    Jobsarchived4.objects.filter(**query).only(*self.onlyColumns), \
                    Jobsarchived.objects.filter(**query).only(*self.onlyColumns) \
            )
#            _django_logger.debug('filter_queryset: after filtered qs')
        else:
#            _django_logger.debug('filter_queryset: before initial qs')
            qs = self.get_initial_queryset()
#            _django_logger.debug('filter_queryset: before initial qs')
#        _logger.debug('|qs|=%d' % (qs.count()))
        return qs


    def filterModel(self, query):
        """
            filterModel
                filter qs or querychain with the query
        """
        _logger.debug('filterModel query: %s' % (str(query)))
        print 'filterModel query: %s' % (str(query))
        ### add constraint that jeditaskid is not NULL
        query['jeditaskid__isnull'] = False
        return QuerySetChain(\
            Jobsdefined4.objects.filter(**query), \
            Jobsactive4.objects.filter(**query), \
            Jobswaiting4.objects.filter(**query), \
            Jobsarchived4.objects.filter(**query), \
            Jobsarchived.objects.filter(**query) \
        )


    def paging(self, qs):
        """ Paging
        """
        limit = min(int(self.request.REQUEST.get('iDisplayLength', 300)), self.max_display_length)
        # if pagination is disabled ("bPaginate": false)
        if limit == -1:
#            _logger.debug('limit==-1, qs=' + str(qs))
            _logger.debug('limit==-1')
            return qs
        start = int(self.request.REQUEST.get('iDisplayStart', 0))
        offset = start + limit
#        _logger.debug('limit>-1, qs=' + str(qs) + ' start=' + str(start) + ' offset=' + str(offset))
        _logger.debug('limit>-1, start=' + str(start) + ' offset=' + str(offset))
        return qs[start:offset]


    def get_context_data(self, smry=0, *args, **kwargs):
        ret = {}
        ### get original dict for datatables
        request = self.request
        self.initialize(*args, **kwargs)

        qs = self.get_initial_queryset()
#        _logger.debug('get_context_data:qs=%s' % (str(qs)))

        # number of records before filtering
        total_records = qs.count()

        qs = self.filter_queryset(qs)
#        _logger.debug('get_context_data:qs=%s' % (str(qs)))

        # number of records after filtering
        total_display_records = qs.count()

        qs = self.ordering(qs)
#        _logger.debug('get_context_data:qs=%s' % (str(qs)))

#        if 'smry' not in self.request.POST.keys():
#            qs = self.paging(qs)
#        _logger.debug('get_context_data:smry=%s' % (str(smry)))
        if not smry:
            qs = self.paging(qs)
        else:
            qs = self.paging(qs).get()
#        _logger.debug('get_context_data:qs=%s' % (str(qs)))

        # prepare output data
        aaData = self.prepare_results(qs)

        _logger.debug('get_context_data')

        ret = {'sEcho': int(request.REQUEST.get('sEcho', 0)),
               'iTotalRecords': total_records,
               'iTotalDisplayRecords': total_display_records,
               'aaData': aaData
               }

        _logger.debug('get_context_data')
        _logger.debug('get_context_data aaData=' + str(aaData))

        if smry:
            (smry, smrykeys) = self.getSummary(aaData)
            ret['aaData'] = smry
            ret['aaDataKeys'] = smrykeys
            _logger.debug('ret=' + str(ret))

        ### correct for wrong/too small iTotalRecords from the default queryset
        try:
            if ret['iTotalRecords'] < ret['iTotalDisplayRecords']:
                ret['iTotalRecords'] = ret['iTotalDisplayRecords']
        except:
            _logger.error('Failed to change iTotalRecords(%s) to iTotalDisplayRecords(%s)'\
                          % (ret['iTotalRecords'], ret['iTotalDisplayRecords']))

        ret['filter'] = str(self.queryDict)

        return ret



