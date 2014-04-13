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
from ...common.models import Users
from ...common.utils import QuerySetChain, subDict, getFilterFieldRenderText, \
    getFilterNameForField
#from .serializers import SerializerPandaJob
from ..jedi.jobsintask.views import PandaJobDictJsonJobsInTask, \
    PandaJobDictJsonJobsInTaskSummary
from ...table.views import ModelJobDictJson
from .serializers import SerializerUsers

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
LAST_N_DAYS_USER = FILTER_UI_ENV['USERDAYS']
LAST_N_HOURS = FILTER_UI_ENV['HOURS']
LAST_N_DAYS_MAX = FILTER_UI_ENV['MAXDAYS']
LAST_N_DAYS_MAX_USER = FILTER_UI_ENV['USERMAXDAYS']


#_logger = logging.getLogger(__name__)
_logger = logging.getLogger('user_views')
_django_logger = logging.getLogger('django')

#currentDateFormat = "%Y-%m-%d %H:%M:%SZ"
currentDateFormat = defaultDatetimeFormat
shortUIDateFormat = "%m-%d %H:%M"


class ListActiveUsersDictJson(PandaJobDictJsonJobsInTask):
#class ListActiveUsersDictJson(ModelJobDictJson):
    """
        ListActiveUsersDictJson
            reverse url: api-datatables-user-list-active-users
    """
    # The model we're going to show
#    model = PandaJob
    model = Users

    # reverse URL
    reverseUrl = 'api-datatables-user-list-active-users'

    # Define subset of columns to be used in this resource
    # define the columns that will be returned
    columns = COLUMNS[reverseUrl]
    filterFields = FILTERS[reverseUrl]
    onlyColumns = list(set(COLUMNS[reverseUrl] + SUMMARY_FIELDS[reverseUrl]))
    summaryColumns = SUMMARY_FIELDS[reverseUrl]

    # define column names that will be used in sorting
    # order is important and should be same as order of columns
    # displayed by datatables. For non sortable columns use empty
    # value like ''
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
        serializer = SerializerUsers(qs, many=True, fields=self.columns)
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
        ### limit modificationtime range
        startdate = datetime.utcnow() - timedelta(days=LAST_N_DAYS_MAX_USER)
        startdate = startdate.strftime(defaultDatetimeFormat)
        enddate = datetime.utcnow().strftime(defaultDatetimeFormat)
        ### get the initial queryset properties
        query = {\
            'lastmod__range': [startdate, enddate]
        }
        ### get the initial queryset
        qs = Users.objects.filter(**query).only(*self.onlyColumns)
        ### return the initial queryset
        return qs


#    def filter_queryset(self, qs):
##        return self.get_initial_queryset()
#        return qs


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

        qs = self.paging(qs)
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
#        _logger.debug('get_context_data aaData=' + str(aaData))

        ### correct for wrong/too small iTotalRecords from the default queryset
        try:
            if ret['iTotalRecords'] < ret['iTotalDisplayRecords']:
                ret['iTotalRecords'] = ret['iTotalDisplayRecords']
        except:
            _logger.error('Failed to change iTotalRecords(%s) to iTotalDisplayRecords(%s)'\
                          % (ret['iTotalRecords'], ret['iTotalDisplayRecords']))
        return ret



def isQueryTimeLimited(query):
    ret = False
    for key in query:
        if not ret and key.startswith('modificationtime'):
            ret = True
    return ret



class ListUsersActivityDictJson(PandaJobDictJsonJobsInTask):
    # The model we're going to show
    model = PandaJob

    # reverse URL
    reverseUrl = 'api-datatables-user-list-user-activity'

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


    def get_initial_queryset(self):
        """
            get_initial_queryset: override this because PanDA job 
                                  is described by 4 different models
        
        """
        ### limit modificationtime range
        startdate = datetime.utcnow() - timedelta(days=LAST_N_DAYS_USER)
        startdate = startdate.strftime(defaultDatetimeFormat)
        enddate = datetime.utcnow().strftime(defaultDatetimeFormat)
        _logger.debug('get_initial_queryset')
#        _logger.debug('get_initial_queryset: self.request' + str(self.request))
        # use request parameters to filter queryset
        ### get the POST keys
        POSTkeys = self.request.POST.keys()
#        ### assemble query from POST parameters for the filter
        queryPost = self.getFilterFromPost(POSTkeys)
        ### get the initial queryset properties
        query = {\
            'modificationtime__range': [startdate, enddate]
        }
        if 'produsername' in queryPost:
            query['produsername'] = queryPost['produsername']
        _logger.debug('query: %s' % (str(query)))
        ### get the initial queryset
        qs = QuerySetChain(\
            Jobsdefined4.objects.filter(**query).only(*self.onlyColumns), \
            Jobsactive4.objects.filter(**query).only(*self.onlyColumns), \
            Jobswaiting4.objects.filter(**query).only(*self.onlyColumns), \
            Jobsarchived4.objects.filter(**query).only(*self.onlyColumns) \
        )
#        _django_logger.debug('get_initial_queryset: after qs')
        ### return the initial queryset
        return qs


    def filter_queryset(self, qs):
#        _logger.debug('filter_queryset qs: %s' % (str(qs)))
#        _logger.debug('filter_queryset: caller name:' + str(inspect.stack()[1][3]))
        # use request parameters to filter queryset
        ### get the POST keys
        POSTkeys = self.request.POST.keys()
        ### see if we filtered from UI
        ### if pgst in self.request.POST --> filtered from UI
        pgst = ''
        if 'pgst' in POSTkeys:
            pgst = self.request.POST['pgst']
        if pgst == 'ini':
#            _logger.debug('|qs|=%d' % (qs.count()))
            return qs
#        ### assemble query from POST parameters for the filter
        query = self.getFilterFromPost(POSTkeys)
        _logger.debug('query: %s' % (str(query)))
        ### execute filter on the queryset
#        _django_logger.debug('filter_queryset: pgst=' + str(pgst))
        if pgst in ['fltr'] and query != {}:
            if not isQueryTimeLimited(query):
                ### limit modificationtime range
                startdate = datetime.utcnow() - timedelta(days=LAST_N_DAYS_USER)
                startdate = startdate.strftime(defaultDatetimeFormat)
                enddate = datetime.utcnow().strftime(defaultDatetimeFormat)
                ### get the initial queryset properties
                query['modificationtime__range'] = [startdate, enddate]
##            ### add constraint that jeditaskid is not NULL
##            query['jeditaskid__isnull'] = False
            qs = QuerySetChain(\
                    Jobsdefined4.objects.filter(**query).only(*self.onlyColumns), \
                    Jobsactive4.objects.filter(**query).only(*self.onlyColumns), \
                    Jobswaiting4.objects.filter(**query).only(*self.onlyColumns), \
                    Jobsarchived4.objects.filter(**query).only(*self.onlyColumns) \
            )
#            _django_logger.debug('filter_queryset: after filtered qs')
        else:
#            _django_logger.debug('filter_queryset: before initial qs')
            qs = self.get_initial_queryset()
#            _django_logger.debug('filter_queryset: before initial qs')
#        _logger.debug('|qs|=%d' % (qs.count()))
        return qs


#class ListUsersActivitySmryDictJson(PandaJobDictJsonJobsInTask):
class ListUsersActivitySmryDictJson(ListUsersActivityDictJson):
    max_display_length = -1
    # The model we're going to show
    model = PandaJob
#    onlyColumns = list(set(COLUMNS[self.reverseUrl] + SUMMARY_FIELDS[self.reverseUrl]))


    def getSummary(self, data):
        """
            get summary data for view self.reverseUrl
            
        """
        return self.getSummarySmry(data)


    def getAnnotationForQuery(self, query, smryFields):
        _logger.debug('getAnnotationForQuery: mark')
        _django_logger.debug('getAnnotationForQuery: mark')
        annotationQuery = {}
        for smryField in smryFields:
            smryCntName = '%s__count' % (smryField)
            _logger.debug('getAnnotationForQuery: smryField=' + smryField)
            annotationQuery[smryCntName] = Count(smryField, distinct=False)
        _logger.debug('getAnnotationForQuery mark')
        ### annotation queryset as a list of  dictionaries -> values
        qs = QuerySetChain(\
                Jobsactive4.objects.filter(**query).values(*smryFields)
                    .annotate(**annotationQuery), \
                Jobsdefined4.objects.filter(**query).values(*smryFields)
                    .annotate(**annotationQuery), \
                Jobswaiting4.objects.filter(**query).values(*smryFields)
                    .annotate(**annotationQuery), \
                Jobsarchived4.objects.filter(**query).values(*smryFields)
                    .annotate(**annotationQuery), \
            )
        _django_logger.debug('getAnnotationForQuery: mark')
        return qs


    def get_initial_queryset(self):
        """
            get_initial_queryset: override this because PanDA job 
                                  is described by 4 different models
        
        """
        _logger.debug('reverseUrl=' + str(self.reverseUrl))
        _logger.debug('columns=' + str(self.columns))
        _logger.debug('filterFields=' + str(self.filterFields))
        _logger.debug('onlyColumns=' + str(self.onlyColumns))
        _logger.debug('summaryColumns=' + str(self.summaryColumns))
        _logger.debug('order_columns=' + str(self.order_columns))
        ### limit modificationtime range
        startdate = datetime.utcnow() - timedelta(days=LAST_N_DAYS_USER)
        startdate = startdate.strftime(defaultDatetimeFormat)
        enddate = datetime.utcnow().strftime(defaultDatetimeFormat)
        _logger.debug('get_initial_queryset')
#        _logger.debug('get_initial_queryset: self.request' + str(self.request))
        # use request parameters to filter queryset
        ### get the POST keys
        POSTkeys = self.request.POST.keys()
#        ### assemble query from POST parameters for the filter
        queryPost = self.getFilterFromPost(POSTkeys)
        ### get the initial queryset properties
        query = {\
            'modificationtime__range': [startdate, enddate]
        }
        if 'produsername' in queryPost:
            query['produsername'] = queryPost['produsername']
        _logger.debug('query: %s' % (str(query)))
        ### get annotation for the initial queryset
        qs = self.getAnnotationForQuery(query, self.summaryColumns)
#        _logger.debug('qs: %s' % (str(qs)))
        ### return annotation queryset
        return qs


    def filter_queryset(self, qs):
        """
            filter_queryset
            @param: qs ... queryset to further filter
            @returns: filtered queryset
        """
        # use request parameters to filter queryset
        ### get the POST keys
        POSTkeys = self.request.POST.keys()
        ### see if we filtered from UI
        ### if pgst in self.request.POST --> filtered from UI
        pgst = ''
        if 'pgst' in POSTkeys:
            pgst = self.request.POST['pgst']
        if pgst == 'ini':
#            _logger.debug('|qs|=%d' % (qs.count()))
            return qs
        ### assemble query from POST parameters for the filter
        query = self.getFilterFromPost(POSTkeys)
        _logger.debug('query: %s' % (str(query)))
        ### execute filter on the queryset
        if pgst in ['fltr'] and query != {}:
            _logger.debug('mark')
            if not isQueryTimeLimited(query):
#                _logger.debug('mark')
                ### limit modificationtime range
                startdate = datetime.utcnow() - timedelta(days=LAST_N_DAYS_USER)
                startdate = startdate.strftime(defaultDatetimeFormat)
                enddate = datetime.utcnow().strftime(defaultDatetimeFormat)
                ### get the initial queryset properties
                query['modificationtime__range'] = [startdate, enddate]
#                _logger.debug('mark')
##            ### add constraint that jeditaskid is not NULL
##            query['jeditaskid__isnull'] = False
#            ### add constraint that jeditaskid is not NULL
#            query['jeditaskid__isnull'] = False
#            _logger.debug('mark')
#            _logger.debug('self.summaryColumns=' + str(self.summaryColumns))
            qs = self.getAnnotationForQuery(query, self.summaryColumns)
#            _logger.debug('qs=' + str(qs))
#            _logger.debug('mark')
        else:
#            _logger.debug('mark')
            qs = self.get_initial_queryset()
#            _logger.debug('qs=' + str(qs))
#            _logger.debug('mark')
#        _logger.debug('|qs|=%d' % (qs.count()))
        ### return filtered queryset
        return qs


    def get_context_data(self, smry=1, *args, **kwargs):
        ret = super(ListUsersActivitySmryDictJson, self).get_context_data(smry=smry, *args, **kwargs)
        _logger.debug('get_context_data:ret=%s' % (str(ret)))
        return ret


    def prepare_results(self, qs):
        """
            prepare_results super's prepare_results to get list of dicts instead of list of lists
            args:
                qs ... queryset of the model instances
            return:
                list of dicts with data of the qs items
        """
        data = []
        ### qs is annotation of multiple fields from self.summaryColumns
        ###    it is a list of tuples
        for smryField in self.summaryColumns:
            _logger.debug('field:' + smryField)
            cntID = '%s__count' % (smryField)
            smryFieldData = []
            try:
                ### get data for this smryField from the queryset
                smryFieldData = [ { smryField: x[smryField], \
                                       cntID: x[cntID] } \
                                     for x in qs ]
                ### get unique values for smryField
                smryFieldDataKeys = list(set([ x[smryField] for x in smryFieldData]))
                ### calculate number of occurences for each unique value of smryField
                for caption in smryFieldDataKeys:
                    captionSum = sum([x[cntID]
                                          for x in smryFieldData \
                                            if x[smryField] == caption])
                    ### record the summary item
                    data.append(\
                        {\
                            smryField: caption, \
                            cntID: captionSum
                            } \
                    )
            except:
                _logger.error(\
                        'prepare_result: cannot get summary data for field %s' \
                        % (smryField, self.summaryColumns))
        ### return prepared data
        return data

