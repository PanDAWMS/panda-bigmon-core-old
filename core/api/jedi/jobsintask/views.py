""" 
api.jedi.jobsintask.views

"""
import inspect

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
from ....common.utils import QuerySetChain, subDict, getFilterFieldRenderText
from .serializers import SerializerPandaJob

#### BEGIN: for debug purposes only
#from ....htcondor.models import HTCondorJob
#from .serializers import SerializerHTCondorJob
#from .utils import isSecure, getDN, getFQAN, getRemoteHost, checkBanUser
#import status as htcondorapi_status
#### END: for debug purposes only


from ....table.views import ModelJobDictJson, VALUE_ALL_MULTISTRING
#from ..common.settings import STATIC_URL, FILTER_UI_ENV, defaultDatetimeFormat
from ....common.settings import FILTER_UI_ENV, defaultDatetimeFormat
from ....pandajob.columns_config import COLUMNS, ORDER_COLUMNS, COL_TITLES, FILTERS, SUMMARY_FIELDS
LAST_N_DAYS = FILTER_UI_ENV['DAYS']
LAST_N_HOURS = FILTER_UI_ENV['HOURS']
LAST_N_DAYS_MAX = FILTER_UI_ENV['MAXDAYS']


#_logger = logging.getLogger(__name__)
_logger = logging.getLogger('jedi_jobsintask')

currentDateFormat = "%Y-%m-%d %H:%M:%SZ"
shortUIDateFormat = "%m-%d %H:%M"


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
                        valueStr = value.strftime(shortUIDateFormat)
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
        _logger.debug('prepare_results: caller name:' + str(inspect.stack()[1][3]))
        ### original prepare_results provides data as list of lists
        ### overridden prepare_results, with data as list of dicts
        _logger.debug('qs=' + str(qs))
        serializer = SerializerPandaJob(qs, many=True)
        _logger.debug('mark')
        data = serializer.data
        _logger.debug('|data|=' + str(len(data)))
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
        _logger.debug('get_initial_queryset: caller name:' + str(inspect.stack()[1][3]))
###DEBUG###        startdate = datetime.utcnow() - timedelta(hours=LAST_N_HOURS)
###DEBUG###        startdate = datetime.utcnow() - timedelta(days=LAST_N_DAYS)
###DEBUG###        startdate = datetime.utcnow() - timedelta(minutes=1)
#        startdate = datetime.utcnow() - timedelta(hours=LAST_N_HOURS)
        startdate = datetime.utcnow() - timedelta(days=LAST_N_DAYS)
        startdate = startdate.strftime(defaultDatetimeFormat)
        enddate = datetime.utcnow().strftime(defaultDatetimeFormat)
        _logger.debug('get_initial_queryset')
        qs = QuerySetChain(\
                    Jobsdefined4.objects.filter(\
                        modificationtime__range=[startdate, enddate]\
                        , jeditaskid__isnull=False \
                    ), \
                    Jobsactive4.objects.filter(\
                        modificationtime__range=[startdate, enddate]\
                        , jeditaskid__isnull=False \
                    ), \
                    Jobswaiting4.objects.filter(\
                        modificationtime__range=[startdate, enddate]\
                        , jeditaskid__isnull=False \
                    ), \
#                    Jobsarchived4.objects.filter(\
#                        modificationtime__range=[startdate, enddate]\
#                    ), \
            )
#        qs = QuerySetChain(\
#                    Jobsactive4.objects.filter(\
#                            jeditaskid=4000195, \
##                            modificationtime__range=[startdate, enddate], \
#                    ), \
#            )
        return qs


#    def filter_querysetOld(self, qs):
#        # use request parameters to filter queryset
#        ### get the POST keys
#        POSTkeys = self.request.POST.keys()
#        _logger.debug('POSTkeys=' + str(POSTkeys))
#        _logger.debug('POSTvalues=' + str(self.request.POST))
#        qs = QuerySetChain(\
#                    Jobsactive4.objects.filter(\
#                            jeditaskid=4000195, \
##                            modificationtime__range=[startdate, enddate], \
#                    ), \
#            )
#        return qs


    def filter_queryset(self, qs):
        _logger.debug('filter_queryset: caller name:' + str(inspect.stack()[1][3]))
        # use request parameters to filter queryset
        ### get the POST keys
        POSTkeys = self.request.POST.keys()
        ### see if we filtered from UI
        ### if pgst in self.request.POST --> filtered from UI
        pgst = ''
        if 'pgst' in POSTkeys:
            pgst = self.request.POST['pgst']
        if pgst == 'ini':
            _logger.debug('|qs|=%d' % (qs.count()))
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
        query = self.cleanupDatetimeRange(POSTkeys, query)
        _logger.debug('query: %s' % (str(query)))
        ### execute filter on the queryset
        if pgst in ['fltr'] and query != {}:
            qs = QuerySetChain(\
#                    Jobsdefined4.objects.filter(**query), \
                    Jobsactive4.objects.filter(**query), \
#                    Jobswaiting4.objects.filter(**query), \
                    Jobsarchived4.objects.filter(**query) \
            )
        else:
            qs = self.get_initial_queryset()
        _logger.debug('|qs|=%d' % (qs.count()))
        return qs


    def filterModel(self, query):
        """
            filterModel
                filter qs or querychain with the query
        """
        _logger.debug('query: %s' % (str(query)))
        return QuerySetChain(\
##                    Jobsactive4.objects.filter(\
##                            jeditaskid=4000195, \
##                            modificationtime__range=[startdate, enddate], \
##                    ), \
#                    Jobsdefined4.objects.filter(**query), \
                    Jobsactive4.objects.filter(**query), \
#                    Jobswaiting4.objects.filter(**query), \
                    Jobsarchived4.objects.filter(**query) \
            )


    def paging(self, qs):
        """ Paging
        """
        limit = min(int(self.request.REQUEST.get('iDisplayLength', 10)), self.max_display_length)
        # if pagination is disabled ("bPaginate": false)
        if limit == -1:
            _logger.debug('limit==-1, qs=' + str(qs))
            return qs
        start = int(self.request.REQUEST.get('iDisplayStart', 0))
        offset = start + limit
        _logger.debug('limit>-1, qs=' + str(qs) + ' start=' + str(start) + ' offset=' + str(offset))
        return qs[start:offset]


    def getSummary(self, data):
        """
            get summary data for view self.reverseUrl
            
        """
        return (data, {})


    def get_context_data(self, smry=0, *args, **kwargs):
        ret = {}
        ### get original dict for datatables
        request = self.request
        self.initialize(*args, **kwargs)

        qs = self.get_initial_queryset()
        _logger.debug('get_context_data:qs=%s' % (str(qs)))

        # number of records before filtering
        total_records = qs.count()

        qs = self.filter_queryset(qs)
        _logger.debug('get_context_data:qs=%s' % (str(qs)))

        # number of records after filtering
        total_display_records = qs.count()

        qs = self.ordering(qs)
        _logger.debug('get_context_data:qs=%s' % (str(qs)))

#        if 'smry' not in self.request.POST.keys():
#            qs = self.paging(qs)
        _logger.debug('get_context_data:smry=%s' % (str(smry)))
        if not smry:
            qs = self.paging(qs)
        else:
            qs = self.paging(qs).get()
        _logger.debug('get_context_data:qs=%s' % (str(qs)))

        # prepare output data
        aaData = self.prepare_results(qs)

        _logger.debug('get_context_data')

        ret = {'sEcho': int(request.REQUEST.get('sEcho', 0)),
               'iTotalRecords': total_records,
               'iTotalDisplayRecords': total_display_records,
               'aaData': aaData
               }

        if smry:
            (smry, smrykeys) = self.getSummary(aaData)
            ret['aaData'] = smry
            ret['aaDataKeys'] = smrykeys

        ### correct for wrong/too small iTotalRecords from the default queryset
        try:
            if ret['iTotalRecords'] < ret['iTotalDisplayRecords']:
                ret['iTotalRecords'] = ret['iTotalDisplayRecords']
        except:
            _logger.error('Failed to change iTotalRecords(%s) to iTotalDisplayRecords(%s)'\
                          % (ret['iTotalRecords'], ret['iTotalDisplayRecords']))
        return ret



class PandaJobDictJsonJobsInTaskSummary(PandaJobDictJsonJobsInTask):
    max_display_length = -1
    # The model we're going to show
    model = PandaJob


    def getSummaryForField(self, summaryField, data):
        """
            get summary dict for field summaryField from data
            
        """
        res = {}
        uniqueValues = []
        try:
            uniqueValues = list(set([ item[summaryField] for item in data ]))
        except:
            pass
        res = dict([(v,
                     len([item[summaryField] for item in data
                          if v == item[summaryField]])
                     ) for v in uniqueValues])
        _logger.debug('field: ' + summaryField + ' res=' + str(res))
        return res


    def getSummary(self, data):
        """
            get summary data for view self.reverseUrl
            
        """
        _logger.debug('getSummary:POSTkeys=%s' % (str(self.request.POST.keys())))
        summary = {}
        smrykeys = {}
        for summaryField in SUMMARY_FIELDS[self.reverseUrl]:
            summaryFieldResult = []
            summaryFieldResult = self.getSummaryForField(summaryField, data)
            if len(summaryFieldResult) > 0:
                summaryFieldRenderText = getFilterFieldRenderText(summaryField, COL_TITLES[self.reverseUrl])
                summary[summaryFieldRenderText] = summaryFieldResult
                smrykeys[summaryFieldRenderText] = summaryField
        return (summary, smrykeys)


    def get_context_data(self, smry=1, *args, **kwargs):
        ret = super(PandaJobDictJsonJobsInTaskSummary, self).get_context_data(smry=smry, *args, **kwargs)
        _logger.debug('get_context_data:ret=%s' % (str(ret)))
        return ret


