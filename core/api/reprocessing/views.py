""" 
api.reprocessing.views

"""
from datetime import datetime, timedelta
import logging
import pytz
import re
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
#from snippets.models import Snippet
#from snippets.serializers import SnippetSerializer
from ...common.models import JediTasks
from ...common.settings import FILTER_UI_ENV, defaultDatetimeFormat
from ...common.utils import QuerySetChain  #, subDict, getFilterFieldRenderText, \
#    getFilterNameForField
from ...pandajob.models import PandaJob, Jobsactive4, Jobsdefined4, \
    Jobswaiting4, Jobsarchived4, Jobsarchived
from ...pandajob.serializers import SerializerPandaJobReprocessing  # ,SerializerPandaJob
from ...pandajob.columns_config import COLUMNS, ORDER_COLUMNS, \
    COL_TITLES, SMRYCOL_TITLES, FILTERS, SUMMARY_FIELDS
from ...table.views import VALUE_ALL_MULTISTRING, INTERVALWILDCARDS, WILDCARDS, \
    currentDateFormat, currentDateFormatPost
LAST_N_DAYS = FILTER_UI_ENV['DAYS']
LAST_N_HOURS = FILTER_UI_ENV['HOURS']
LAST_N_DAYS_MAX = FILTER_UI_ENV['MAXDAYS']
_logger = logging.getLogger('api_reprocessing')
_django_logger = logging.getLogger('django')

#currentDateFormat = "%Y-%m-%d %H:%M:%SZ"
#currentDateFormat = defaultDatetimeFormat
#shortUIDateFormat = "%m-%d %H:%M"

# reverse URL
reverseUrl = 'api-reprocessing-jobs-in-task-smry'
model = PandaJob
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


def cleanupDatetimeRange(requestKeys, queryDict):
    """
        cleanupDatetimeRange 
        ... in queryDict merge submitted__lte and submitted__gte filter 
            fields into submitted__range for all datetime type fields 
            (e.g. submitted)
                
    """
    _logger.debug('incoming queryDict=' + str(queryDict))
    datetimeFilters = [ x for x in model._meta.filterFields \
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
        ### decide whether there is info for range or half-range in the request keys
        if fNameFrom in requestKeys or fNameTo in requestKeys:
            ### interval start
            if fFilterFieldFrom and fFilterFieldFrom in queryDict.keys():
                rangeFrom = queryDict[fFilterFieldFrom]
                del queryDict[fFilterFieldFrom]
            else:
                rangeFrom = datetime.utcnow() - timedelta(hours=LAST_N_HOURS)
                rangeFrom = rangeFrom.replace(tzinfo=pytz.UTC, microsecond=0)
            ### interval end
            if fFilterFieldTo and fFilterFieldTo in queryDict.keys():
                rangeTo = queryDict[fFilterFieldTo]
                del queryDict[fFilterFieldTo]
            else:
                rangeTo = datetime.utcnow()
                rangeTo = rangeTo.replace(tzinfo=pytz.UTC, microsecond=0)
            ### range instead
            queryDict[datetimeField + '__range'] = [rangeFrom, rangeTo]
    _logger.debug('outgoing queryDict=' + str(queryDict))
    return queryDict


def getQueryValueDatetime(fName, fValue):
    """
            getQueryValueDatetime
    """
    print ':120 fvalue=', fValue
    print ':120 format=', currentDateFormatPost
    try:
        fValue = datetime.strptime(fValue, currentDateFormatPost).replace(tzinfo=pytz.UTC)
        print ":124"
        return fValue
    except:
        print ":127"
        _logger.error('Unknown datetime format for filter ' + \
                                    'field [%s] with value [%s].' % (fName, fValue))
        try:
            print ":131"
            fValue = re.sub(' ', 'T', fValue) + ':00Z'
            print ":133"
            fValue = datetime.strptime(fValue, currentDateFormatPost).replace(tzinfo=pytz.UTC)
            print ":135"
        except ValueError:
            print ":137"
            ### unknown datetime format
            _logger.error('Unknown datetime format for filter ' + \
                                    'field [%s] with value [%s].' % (fName, fValue))
    return fValue


def getQueryValueStringWildcard(fValue):
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


def getQueryValueStringmultiple(fName, fValue):
    """
        getQueryValueStringmultiple
    """
    valList = fValue.split(',')
    if VALUE_ALL_MULTISTRING in valList:
        return (VALUE_ALL_MULTISTRING, '')
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


def getQueryValueIntIntervalWildcard(self, fValue):
    """
        getQueryValueIntIntervalWildcard
        e.g. wmsid == '1801'
            intervals:      '1801:1805' ... xrange(1801, 1805+1)
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


def getFilterForTaskname(fName, fValue):
    query = {}
    retVal = getQueryValueStringWildcard(fValue)
    for val, suffix in retVal:
        query['%s%s' % (fName, suffix)] = val
    return query


def getFilterFromRequest(request, requestKeys):
    """
        getFilterFromRequest -- prepare query for queryset
    """
    ### assemble query from POST parameters for the filter
    print 'Entered getFilterFromRequest'
    query = {}
    for filterField in filterFields:
        fName = filterField['name']
        if fName in requestKeys:
            fValue = ''
            if fName in request.POST:
                fValue = request.POST[fName]
            elif fName in request.GET:
                fValue = request.GET[fName]
            fField = filterField['field']
            fFilterField = filterField['filterField']
            fType = filterField['type']
            ### process datetime types
            if fType == 'datetime':
                fValue = getQueryValueDatetime(fName, fValue)
                query.update({'%s' % (fFilterField) : fValue})
            ### process string with multiple selection
            elif fType == 'stringMultiple':
                val, suffix = getQueryValueStringmultiple(fName, fValue)
                ### val=='all'==VALUE_ALL_MULTISTRING,
                ### if VALUE_ALL_MULTISTRING is selected among values
                ###     then do not filter by this fField
                if val != VALUE_ALL_MULTISTRING:
                    query['%s%s' % (fField, suffix)] = val
            ### process wildcarded strings
            elif fType == 'string':
                retVal = getQueryValueStringWildcard(fValue)
                for val, suffix in retVal:
                    query['%s%s' % (fField, suffix)] = val
            ### process wildcarded integers
            elif fType == 'integer':
                retVal = getQueryValueIntIntervalWildcard(fValue)
                for val, suffix in retVal:
                    query['%s%s' % (fField, suffix)] = val
            ### process anything else
            else:
                query.update({'%s' % (fFilterField) : fValue})
    ### cleanup for datetime ranges
    query = cleanupDatetimeRange(requestKeys, query)
    ### return query dict
    return query


def get_initial_queryset():
    ### limit modificationtime range
    startdate = datetime.utcnow() - timedelta(minutes=5)
    startdate = startdate.strftime(defaultDatetimeFormat)
    enddate = datetime.utcnow().strftime(defaultDatetimeFormat)
    ### get the initial queryset properties
    query = {\
        'modificationtime__range': [startdate, enddate]
    }
    ### get the initial queryset
    qs = QuerySetChain(\
            Jobsdefined4.objects.filter(**query).only(*onlyColumns), \
            Jobsactive4.objects.filter(**query).only(*onlyColumns), \
            Jobswaiting4.objects.filter(**query).only(*onlyColumns), \
            Jobsarchived4.objects.filter(**query).only(*onlyColumns), \
            Jobsarchived.objects.filter(**query).only(*onlyColumns) \
    )
    return (qs, query)


def filter_queryset(request, qs):
    # use request parameters to filter queryset
    ### get the POST keys
#    POSTkeys = request.POST.keys()
    GETkeys = request.GET.keys()
#    ### see if we filtered from UI
#    ### if pgst in self.request.POST --> filtered from UI
#    pgst = 'fltr'
#    if 'pgst' in POSTkeys:
#        pgst = request.POST['pgst']
#    elif 'pgst' in GETkeys:
#        pgst = request.GET['pgst']
#    if pgst == 'ini':
#        return qs
    ### handle the taskname filter: taskname is not a field of Jobs object
    qs_taskname_ids = []
    taskname_query = {}
    taskname_query_val = ''
#    if 'taskname' in POSTkeys:
#        try:
#            taskname_query_val = request.POST['taskname']
#            del request.POST['taskname']
#        except:
#            _logger.error('Cannot remove "taskname" entry from the query: %s' % (str(POSTkeys)))
#    el
    if 'taskname' in GETkeys:
        try:
            taskname_query_val = request.GET['taskname']
            del request.GET['taskname']
        except:
            _logger.error('Cannot remove "taskname" entry from the query: %s' % (str(GETkeys)))
    taskname_query = getFilterForTaskname('taskname', taskname_query_val)
    _logger.debug('taskname_query: %s' % (str(taskname_query)))

    qs_taskname_ids = []
    if taskname_query:
        qs_taskname_ids = JediTasks.objects.filter(**taskname_query).values_list('jeditaskid', flat=True)
    _logger.debug('taskname_query: %s' % (str(taskname_query)))
    _logger.debug('qs_taskname_ids: %s' % (str(qs_taskname_ids)))
    ### assemble query from requests' POST/GET parameters for the filter
    # TODO:
#    query_post = self.getFilterFromRequest(request, POSTkeys)
    query_get = getFilterFromRequest(request, GETkeys)
    query = {}
#    query.update(query_post)
    query.update(query_get)
    _logger.debug('query: %s' % (str(query)))
    if len(qs_taskname_ids):
        query['jeditaskid__in'] = qs_taskname_ids
    _logger.debug('query: %s' % (str(query)))
    queryDict = {}
    queryDict.update(query)
    if taskname_query:
        queryDict.update(taskname_query)
    ### execute filter on the queryset
#    if pgst in ['fltr'] and query != {}:
    if query != {}:
        ### add constraint that jeditaskid is not NULL
        _django_logger.debug('filter_queryset: before filtered qs')
        qs = QuerySetChain(\
                Jobsdefined4.objects.filter(**query).only(*onlyColumns), \
                Jobsactive4.objects.filter(**query).only(*onlyColumns), \
                Jobswaiting4.objects.filter(**query).only(*onlyColumns), \
                Jobsarchived4.objects.filter(**query).only(*onlyColumns), \
                Jobsarchived.objects.filter(**query).only(*onlyColumns) \
        )
    else:
        qs, queryDict = get_initial_queryset()
    return qs, queryDict




@api_view(['GET'])
def reprocessing_jobs_in_task_pattern(request):
    """
    Retrieve, update or delete a snippet instance.
    """
    qs, query = get_initial_queryset()
    print ':373 qs=', qs
    qs, query = filter_queryset(request, qs)
    print ':375 qs=', qs

    if not qs.count():
        return Response({})

    try:
        jobs = qs.get()
#    except PandaJob.DoesNotExist:
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SerializerPandaJobReprocessing(jobs, many=True)
        return Response({'data': serializer.data, 'filter': query})

