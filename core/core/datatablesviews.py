""" 
datatablesviews -- parent class for json views for datatables

"""
import json
import logging
import pytz
import re
from datetime import datetime, timedelta
from django_datatables_view.base_datatable_view import BaseDatatableView
from ..settings import FILTER_UI_ENV
from ..htcondor.models import HTCondorJob
from ..api.htcondorapi.serializers import SerializerHTCondorJob

#_logger = logging.getLogger(__name__)
_logger = logging.getLogger('bigpandamon')

currentDateFormat = "%Y-%m-%d %H:%M:%SZ"
currentDateFormatPost = "%Y-%m-%dT%H:%M:%SZ"
VALUE_TRANSLATION = { \
    'lt': '<', \
    'gt': '>', \
}
WILDCARDS = FILTER_UI_ENV['WILDCARDS']
INTERVALWILDCARDS = FILTER_UI_ENV['INTERVALWILDCARDS']
LAST_N_HOURS = FILTER_UI_ENV['HOURS']


class ModelJobDictJson(BaseDatatableView):
    """
        ModelJobDictJson ... prepare datatables view for your favourite Model
        
        ModelJobDictJson is intended for HTCondorJob instances by default. 
        For other models inherit ModelJobDictJson and override
            model
            columns
            order_columns
            max_display_length
            get_initial_queryset() ... due to PanDA jobs over several tables,
                                       queryset vs. QueryChain
            prepare_results()      ... due to different serializer
            get_context_data()     ... due to different "self" in child class
            filterModel()          ... due to PanDA jobs over several tables,
                                       queryset vs. QueryChain
            
    """

    # The model we're going to show
    model = HTCondorJob

    # define the columns that will be returned
    columns = HTCondorJob._meta.allColumns

    # define column names that will be used in sorting
    # order is important and should be same as order of columns
    # displayed by datatables. For non sortable columns use empty
    # value like ''
    order_columns = HTCondorJob._meta.orderColumns

    # set max limit of records returned, this is used to protect our site if someone tries to attack our site
    # and make it return huge amount of data
    max_display_length = 500



    def get_initial_queryset(self):
        """
            get_initial_queryset: override this because PanDA job 
                                  is described by 4 different models
        
        """
        _logger.debug('mark')
        _logger.debug('POST:' + str(self.request.POST))
        qs = HTCondorJob.objects.filter(\
                submitted__range=[ \
                    datetime.utcnow() - timedelta(hours=LAST_N_HOURS), \
                    datetime.utcnow(), \
                ] \
        )
        _logger.debug('qs=' + str(qs))
        return qs


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
        serializer = SerializerHTCondorJob(qs, many=True)
        data = serializer.data
        return data


    def get_context_data(self, *args, **kwargs):
        return super(ModelJobDictJson, self).get_context_data(*args, **kwargs)


    def getQueryValueDatetime(self, fName, fValue):
        """
            getQueryValueDatetime
        """
        try:
            fValue = re.sub(' ', 'T', fValue) + ':00Z'
            fValue = datetime.strptime(fValue, currentDateFormatPost).replace(tzinfo=pytz.UTC)
        except ValueError:
            ### unknown datetime format
            _logger.error('Unknown datetime format for filter ' + \
                                'field [%s] with value [%s].' % (fName, fValue))
        return fValue


    def getQueryValueStringmultiple(self, fName, fValue):
        """
            getQueryValueStringmultiple
        """
        valList = fValue.split(',')
        ### translate special values from VALUE_TRANSLATION
        for k in VALUE_TRANSLATION.keys():
            if k in valList:
                try:
                    kIndex = valList.index(k)
                    valList[kIndex] = VALUE_TRANSLATION[k]
                except IndexError:
                    _logger.error('Could not find location ' + \
                        'of %s in valList for filter %s' % (k, fName))
                except ValueError:
                    _logger.error('Could not find location ' + \
                        'of %s in valList for filter %s' % (k, fName))
        if len(valList) > 1:
            return (valList, '__in')
        else:
            return (fValue, '')


    def getQueryValueStringWildcard(self, fValue):
        """
            getQueryValueStringWildcard
            e.g. owner == 'plove'
                wildcarded: 'p*l*ve'
        """
        valueString = fValue
        res = []
        for wildCard in WILDCARDS:
            val = valueString.split(wildCard)
            if len(val) <= 1:
                res.append((val[0], ''))
            else:
                if val[0]:
                    res.append((val[0], '__istartswith'))
                if val[-1]:
                    res.append((val[-1], '__iendswith'))
                if len(val) > 2:
                    for x in val[1:-1]:
                        res.append((x, '__icontains'))
        return res


    def getQueryValueIntIntervalWildcard(self, fValue):
        """
            getQueryValueIntIntervalWildcard
            e.g. wmsid == '1801'
                intervals:     '1801:1805' ... xrange(1801, 1805+1)
                               ':1805' ... xrange(0, 1805+1)
                               '1801:' ... xrange(1801, max(wmsid))
        """
        valueString = fValue
        _logger.debug('fValue=' + str(fValue))
        res = []
        for wildCard in INTERVALWILDCARDS:
            val = valueString.split(wildCard)
            _logger.debug('val=' + str(val))
            ### always except from 1 to 2 fields in val
            try:
                vMin = int(val[0])
            except ValueError:
                vMin = None
            try:
                vMax = int(val[-1])
            except ValueError:
                vMax = None
            ### exactly one wmsid, no wildcard for interval present
            if len(val) == 1:
                res.append((vMin, ''))
            ### a wildcard for interval present
            else:
                if vMin:
                    res.append((vMin, '__gte'))
                if vMax:
                    res.append((vMax, '__lte'))
        return res


    def cleanupDatetimeRange(self, POSTkeys, queryDict):
        """
            cleanupDatetimeRange 
            ... in queryDict merge submitted__lte and submitted__gte filter 
                fields into submitted__range for all datetime type fields 
                (e.g. submitted)
                 
        """
        _logger.debug('incoming queryDict=' + str(queryDict))
#        datetimeFilters = [ x for x in HTCondorJob._meta.filterFields \
#                    if x['type'] == 'datetime']
        datetimeFilters = [ x for x in self.model._meta.filterFields \
                    if x['type'] == 'datetime']
        datetimeFields = list(set([ x['field'] for x in datetimeFilters ]))
        for datetimeField in datetimeFields:
            xFilters = [x for x in datetimeFilters \
                        if x['field'] == datetimeField]
            xFilterFields = [(x['name'], x['filterField'])  for x in xFilters]
            ### assume there is always 1 "From" and 1 "To" filter
            ### for a datetime field
            fNameFrom = None
            fNameTo = None
            try:
                fNameFrom = [ x for x, v in xFilterFields \
                            if re.search('From$', x) is not None ][0]
            except IndexError:
                fNameFrom = None
            try:
                fNameTo = [x for x, v in xFilterFields \
                            if re.search('To$', x) is not None ][0]
            except IndexError:
                fNameTo = None
            ### get filter fields for fName{From,To}
            fFilterFieldFrom = ''
            fFilterFieldTo = ''
            try:
                fFilterFieldFrom = [v for k, v in xFilterFields \
                                        if k == fNameFrom ][0]
            except IndexError:
                fFilterFieldFrom = ''
            try:
                fFilterFieldTo = [v for k, v in xFilterFields \
                                        if k == fNameTo ][0]
            except IndexError:
                fFilterFieldTo = ''
            ### decide whether there is info for range or half-range in POST
            if fNameFrom in POSTkeys or fNameTo in POSTkeys:
                ### interval start
                if fFilterFieldFrom and fFilterFieldFrom in queryDict.keys():
                    rangeFrom = queryDict[fFilterFieldFrom]
                    del queryDict[fFilterFieldFrom]
                else:
                    rangeFrom = datetime.utcnow() - timedelta(hours=LAST_N_HOURS)
                ### interval end
                if fFilterFieldTo and fFilterFieldTo in queryDict.keys():
                    rangeTo = queryDict[fFilterFieldTo]
                    del queryDict[fFilterFieldTo]
                else:
                    rangeTo = datetime.utcnow()
                ### range instead
                queryDict[datetimeField + '__range'] = [rangeFrom, rangeTo]
        _logger.debug('outgoing queryDict=' + str(queryDict))
        return queryDict


    def filterModel(self, query):
        """
            filterModel
                filter qs or querychain with the query
                
                HTCondorJobs: use self.model
                PanDA jobs: use QueryChain trick for querysets
        """
        ### if there is something to filter, then filter with query
        if query.keys():
            return self.model.objects.filter(**query)
        ### otherwise, keep the initial queryset
        else:
            return self.get_initial_queryset()


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
        for filterField in self.model._meta.filterFields:
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
            _logger.debug('query=' + str(query))
            qs = self.filterModel(query)
            _logger.debug('|qs|=%d' % (qs.count()))
        return qs


