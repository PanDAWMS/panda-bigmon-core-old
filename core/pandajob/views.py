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
        getAoColumnsDictWithTitles, QuerySetChain, subDictToStr
#from .datatablesviews import ModelJobDictJson
from ..table.views import ModelJobDictJson
from rest_framework import viewsets
LAST_N_DAYS = FILTER_UI_ENV['DAYS']
LAST_N_HOURS = FILTER_UI_ENV['HOURS']
LAST_N_DAYS_MAX = FILTER_UI_ENV['MAXDAYS']
from .columns_config import COLUMNS, ORDER_COLUMNS, COL_TITLES, FILTERS

#_logger = logging.getLogger(__name__)
_logger = logging.getLogger('bigpandamon')

#currentDateFormat = "%Y-%m-%d %H:%M:%SZ"
currentDateFormat = defaultDatetimeFormat
WILDCARDS = FILTER_UI_ENV['WILDCARDS']
INTERVALWILDCARDS = FILTER_UI_ENV['INTERVALWILDCARDS']
LAST_N_DAYS = FILTER_UI_ENV['DAYS']
LAST_N_HOURS = FILTER_UI_ENV['HOURS']

# Create your views here.
def listJobs(request):
###DEBUG###    startdate = datetime.utcnow() - timedelta(hours=LAST_N_HOURS)
    startdate = datetime.utcnow() - timedelta(minutes=2)
    startdate = startdate.strftime(defaultDatetimeFormat)
    enddate = datetime.utcnow().strftime(defaultDatetimeFormat)
    _logger.debug("startdate = " + str(startdate))
    _logger.debug("enddate = " + str(enddate))
#    jobList = QuerySetChain(\
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
#                            ~ Q(produsername='gangarbt')
#    jobList = QuerySetChain(\
#                    Jobsactive4.objects.filter(\
#                            produsername='gangarbt'
#                        ).filter(\
#                            modificationtime__range=[startdate, enddate]\
#                        ,
#                    ), \
#            )
    jobList = QuerySetChain(\
                    Jobsactive4.objects.filter(\
                            jeditaskid=4000195
                        ,
                    ), \
            )

    _logger.debug('|jobList|=' + str(jobList.count()))
    _logger.debug('jobList[:30]=' + str(jobList[:30]))
    jobList = sorted(jobList, key=lambda x:-x.pandaid)
    _logger.debug('jobList[:30]=' + str(jobList[:30]))
    if request.META.get('CONTENT_TYPE', 'text/plain') == 'text/plain':
        data = {
            'prefix': getPrefix(request),
            'jobList': jobList[:30],
        }
        data.update(getContextVariables(request))
        return render_to_response('pandajob/list_jobs.html', data, RequestContext(request))
    elif request.META.get('CONTENT_TYPE', 'text/plain') == 'application/json':
        resp = []
        for job in jobList:
            resp.append({ 'pandaid': job.pandaid, 'status': job.jobstatus, 'prodsourcelabel': job.prodsourcelabel, 'produserid' : job.produserid})
        return  HttpResponse(json_dumps(resp), mimetype='text/html')


def jobDetails(request, pandaid):
    startdate = datetime.utcnow() - timedelta(days=LAST_N_DAYS_MAX)
    jobs = QuerySetChain(\
        Jobsdefined4.objects.filter(\
            modificationtime__gt=startdate.strftime(defaultDatetimeFormat), \
            pandaid=pandaid\
        ), \
        Jobsactive4.objects.filter(\
            modificationtime__gt=startdate.strftime(defaultDatetimeFormat), \
            pandaid=pandaid\
        ), \
        Jobswaiting4.objects.filter(\
            modificationtime__gt=startdate.strftime(defaultDatetimeFormat), \
            pandaid=pandaid\
        ), \
        Jobsarchived4.objects.filter(\
            modificationtime__gt=startdate.strftime(defaultDatetimeFormat), \
            pandaid=pandaid\
        ), \
    )
    job = {}
    try:
        job = jobs[0]
    except IndexError:
        job = {}
    name = ''
    try:
        name = job['pandaid']
    except:
        name = ''
    if request.META.get('CONTENT_TYPE', 'text/plain') == 'text/plain':
        data = {
            'prefix': getPrefix(request),
            'name': name,
            'job': job,
        }
        data.update(getContextVariables(request))
        return render_to_response('pandajob/details_job.html', data, RequestContext(request))
    elif request.META.get('CONTENT_TYPE', 'text/plain') == 'application/json':
        return  HttpResponse(json_dumps(jobInfo), mimetype='text/html')


def jobInfoDefault(request):
        msg = 'Please provide prodUserName and ndays in your URL, e.g. http://pandawms.org/bigpandamon/job/info/<prodUserName>/<ndays>/'
        data = {
            'prefix': getPrefix(request), \
            'msg': msg \
        }
        data.update(getContextVariables(request))
        return render_to_response('pandajob/msg.html', data, RequestContext(request))


def jobInfo(request, prodUserName, nhours=LAST_N_HOURS):
    _logger.debug('nhours: ...%s...' % (nhours))
    try:
        nhours = int(nhours)
        if (nhours > LAST_N_DAYS_MAX * 24):
            nhours = LAST_N_DAYS_MAX * 24
    except:
        _logger.error('Something wrong with nhours:' + str(nhours))

    ### replace + by space
    _logger.debug('prodUserName: ...%s...' % (prodUserName))
    try:
        prodUserName = re.sub('\+', ' ', prodUserName)
    except:
        pass
    _logger.debug('prodUserName: ...%s...' % (prodUserName))

    jobs = []
    job = {}
    jobKeys = ['pandaid', 'jobstatus', 'cpuconsumptiontime', 'creationtime', 'starttime', \
               'endtime', 'modificationhost', 'computingsite', 'produsername']
    datetimeJobKeys = ['creationtime', 'starttime', 'endtime']
#    try:
#        ndays = int(nhours) * 24
#    except:
#        _logger.error('Something wrong with ndays:' + str(ndays))
    try:
        startdate = datetime.utcnow().replace(tzinfo=pytz.utc) - timedelta(hours=nhours)
    except:
        _logger.error('Something wrong with startdate:')
        startdate = datetime.utcnow().replace(tzinfo=pytz.utc) - timedelta(hours=LAST_N_HOURS)
    startdate = startdate.strftime(defaultDatetimeFormat)
    enddate = datetime.utcnow().replace(tzinfo=pytz.utc).strftime(defaultDatetimeFormat)
    jobs.extend(Jobsactive4.objects.filter(\
                produsername=prodUserName, \
                modificationtime__range=[startdate, enddate] \
    ).values())
    jobs.extend(Jobsdefined4.objects.filter(\
                produsername=prodUserName, \
                modificationtime__range=[startdate, enddate] \
    ).values())
    jobs.extend(Jobswaiting4.objects.filter(\
                produsername=prodUserName, \
                modificationtime__range=[startdate, enddate] \
    ).values())
    jobs.extend(Jobsarchived4.objects.filter(\
                produsername=prodUserName, \
                modificationtime__range=[startdate, enddate] \
    ).values())

    ### Handle json output
    if request.META.get('CONTENT_TYPE', 'text/plain') == 'application/json':
        jobInfo = []
        for job in jobs:
            ### slim job dict
            try:
                newJob = subDictToStr(job, jobKeys, datetimeJobKeys, "%s")
            except:
                _logger.error('Something went wrong with job slimming: keys %s job %s' % (jobKeys, job))
                newJob = job
            ### append job info
            jobInfo.append(newJob)
        return  HttpResponse(json_dumps(jobInfo), content_type="application/json", mimetype='text/html')

    ### Handle other outputs
    name = prodUserName
    jobs = sorted(jobs, key=lambda x:-x['pandaid'])
    data = {
            'prefix': getPrefix(request),
            'jobInfo': jobs, 'name': name, 'nhours': nhours,
    }
    data.update(getContextVariables(request))
    return render_to_response('pandajob/info_jobs.html', data, RequestContext(request))


def jobInfoHours(request, prodUserName, nhours=LAST_N_HOURS):
    return jobInfo(request, prodUserName, nhours)


def jobInfoDays(request, prodUserName, nhours=LAST_N_DAYS * 24):
    return jobInfo(request, prodUserName, nhours * 24)


class JobsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows jobs listed
    """
    def getUrlParams(self, request):
        urlParams = {}
        try:
            urlParams = parse_qs(request.META['QUERY_STRING'])
            for urlParamsKey in urlParams.keys():
                urlParamsKeyLower = urlParamsKey.lower()
                urlParamsKeyData = urlParams[urlParamsKey]
                del urlParams[urlParamsKey]
                urlParams[urlParamsKeyLower] = urlParamsKeyData
        except KeyError:
            urlParams = {}
            _logger.error("Could not find request.META['QUERY_STRING']: META keys are %s" % (request.META.keys()))
        _logger.debug('urlParams=' + str(urlParams))
        return urlParams


    def getJobParamFields(self, urlParams, configJobparam):
        """
        get fields to expose via API
        
        """
        jobparamList = []
        if 'jobparam' in urlParams.keys():
            jobparam = urlParams['jobparam'][0].lower()
            jobparamList = jobparam.split(',')
            for jobparamListItem in jobparamList:
                if jobparamListItem not in configJobparam:
                    try:
                        jobparamList.remove(jobparamListItem)
                    except ValueError:
                        _logger.error('Field %s is not allowed' % (jobparamListItem))
        else:
            jobparamList = configJobparam
        jobparamList = ['pandaid'] + jobparamList
        return jobparamList


    def getProdUserName(self, urlParams):
        """
        get ProdUserName
        
        """
        prodUserName = ""
        if 'produsername' in urlParams.keys():
            prodUserName = urlParams['produsername'][0].lower()
        return prodUserName


    def getDays(self, urlParams):
        """
        get ProdUserName
        
        """
        defaultDaysDiff = 3
        daysDiff = defaultDaysDiff
        if 'days' in urlParams.keys():
            try:
                daysDiff = int(urlParams['days'][0].lower())
            except ValueError:
                daysDiff = defaultDaysDiff
                _logger.error(\
                    'Incorrect format of days field, expected integer, got %s' \
                    % (urlParams['days'][0].lower()) \
                )
        days = datetime.utcnow() - timedelta(days=daysDiff)
        return days


@ensure_csrf_cookie
def list3PandaJobs(request):
    """
        list3PandaJobs -- view to show list of PanDA jobs in a dataTables table
    """
    ### get URL prefix
    prefix = getPrefix(request)
    ### get reverse url of the data view
    dataUrl = reverse('api-datatables-panda-jobs')
    ### get aoColumns pre-config
    aoColumns = [FILTER_UI_ENV['EXPAND_BUTTON']]
    aoColumns += getAoColumnsDictWithTitles(PandaJob._meta.columnTitles)

    data = { \
            'prefix': prefix, \
            'datasrc': str(dataUrl + "?format=json"), \
            'columns': json_dumps(aoColumns), \
    }
    data.update(getContextVariables(request))
    return render_to_response('pandajob/list3.html', data, RequestContext(request))


class PandaJobDictJson(ModelJobDictJson):
    # The model we're going to show
    model = PandaJob

    # define the columns that will be returned
    columns = PandaJob._meta.allColumns

    # define column names that will be used in sorting
    # order is important and should be same as order of columns
    # displayed by datatables. For non sortable columns use empty
    # value like ''
    order_columns = PandaJob._meta.orderColumns

    # set max limit of records returned, this is used to protect our site if someone tries to attack our site
    # and make it return huge amount of data
    max_display_length = 500


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
        _logger.debug('mark')
        return data


    def get_initial_queryset(self):
        """
            get_initial_queryset: override this because PanDA job 
                                  is described by 4 different models
        
        """
        qs = QuerySetChain(\
                    Jobsdefined4.objects.all(), \
                    Jobsactive4.objects.all(), \
                    Jobswaiting4.objects.all(), \
                    Jobsarchived4.objects.all() \
            )
        return qs


    def get_context_data(self, *args, **kwargs):
        return super(PandaJobDictJson, self).get_context_data(*args, **kwargs)


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


@ensure_csrf_cookie
def jediJobsInTask(request):
    """
        list3PandaJobs -- view to show list of PanDA jobs in a dataTables table
                            data from API jedi/jobsintask
    """
    reverseUrl = 'api-datatables-jedi-jobs-in-task'
    ### get URL prefix
    prefix = getPrefix(request)
    ### get reverse url of the data view
    dataUrl = reverse(reverseUrl)
    ### get aoColumns pre-config
#    aoColumns = [FILTER_UI_ENV['EXPAND_BUTTON']]
#    aoColumns += getAoColumnsDictWithTitles(PandaJob._meta.columnTitles)

    aoColumns = []
    aoColumns += getAoColumnsDictWithTitles(COL_TITLES[reverseUrl])

    _logger.debug('columns:')
    data = { \
            'prefix': prefix, \
            'datasrc': str(dataUrl + "?format=json"), \
            'columns': json_dumps(aoColumns), \
    }
    data.update(getContextVariables(request))
    return render_to_response('pandajob/jobsintask.html', data, RequestContext(request))


