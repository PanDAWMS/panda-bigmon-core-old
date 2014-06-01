""" 
views

"""

from json import dumps as json_dumps  ### FIXME - cleanup
import json  ### FIXME - cleanup

import itertools
import logging
import pytz
import re

from datetime import datetime, timedelta
from urlparse import parse_qs, urlparse

from django.db.models import Q, Count
from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django import forms
from django.utils import timezone
from django.conf import settings

from django_datatables_view.base_datatable_view import BaseDatatableView


#from ..settings import CUSTOM_DB_FIELDS, FILTER_UI_ENV
from ..common.settings import STATIC_URL, FILTER_UI_ENV, defaultDatetimeFormat  ### FIXME: use django.conf's settings?
from .models import PandaJob, Jobsactive4, Jobsdefined4, Jobswaiting4, \
    Jobsarchived4, Jobsarchived
from ..common.models import Filestable4, FilestableArch, Users, \
    Jobparamstable, Logstable, JediJobRetryHistory, JediTasks, JediTaskparams, \
    JediEvents

from ..resource.models import Schedconfig
from .serializers import SerializerPandaJob
#from .utils import getPrefix, getContextVariables, \
#        getAoColumnsDictWithTitles, QuerySetChain, subDictToStr
from ..common.utils import getPrefix, getContextVariables, \
        getAoColumnsDictWithTitles, QuerySetChain, subDictToStr, \
        getFilterFieldIDs
#from .datatablesviews import ModelJobDictJson
from ..table.views import ModelJobDictJson
from rest_framework import viewsets
from .columns_config import COLUMNS, ORDER_COLUMNS, COL_TITLES, FILTERS

# from core.common.settings.config import ENV
#### use settings.ENV instead
#from settings.local import dbaccess
#### use settings.DATABASES instead
from .utils import homeCloud, statelist, setupHomeCloud, sitestatelist, \
    viewParams, VOLIST, VONAME, VOMODE, \
    standard_fields, standard_sitefields, standard_taskfields, \
    cleanJobList, cleanTaskList, \
    siteSummaryDict, userSummaryDict, \
    errorInfo, \
    isEventService, \
    siteSummary, voSummary, wnSummary, jobStateSummary, \
    LAST_N_HOURS_MAX, \
    JOB_LIMIT
    # setupView, extensibleURL, userList,

#from django.views.decorators.cache import cache_page

#_logger = logging.getLogger(__name__)
_logger = logging.getLogger('bigpandamon')

#currentDateFormat = "%Y-%m-%d %H:%M:%SZ"
currentDateFormat = defaultDatetimeFormat
WILDCARDS = FILTER_UI_ENV['WILDCARDS']
INTERVALWILDCARDS = FILTER_UI_ENV['INTERVALWILDCARDS']

LAST_N_DAYS = FILTER_UI_ENV['DAYS']  # FIXME: put to utils
LAST_N_HOURS = FILTER_UI_ENV['HOURS']  # FIXME: put to utils
LAST_N_DAYS_MAX = FILTER_UI_ENV['MAXDAYS']  # FIXME: put to utils

# Create your views here.
def listJobs(request):
###DEBUG###    startdate = datetime.utcnow() - timedelta(hours=LAST_N_HOURS)
    startdate = datetime.utcnow() - timedelta(days=LAST_N_DAYS_MAX)
#####    startdate = datetime.utcnow() - timedelta(minutes=2)
    startdate = startdate.strftime(defaultDatetimeFormat)
    enddate = datetime.utcnow().strftime(defaultDatetimeFormat)
    _logger.debug("startdate = " + str(startdate))
    _logger.debug("enddate = " + str(enddate))
    jobList = QuerySetChain(\
                    Jobsdefined4.objects.filter(\
                        modificationtime__range=[startdate, enddate]\
                    ), \
                    Jobsactive4.objects.filter(\
                        modificationtime__range=[startdate, enddate]\
                    ), \
                    Jobswaiting4.objects.filter(\
                        modificationtime__range=[startdate, enddate]\
                    ), \
                    Jobsarchived4.objects.filter(\
                        modificationtime__range=[startdate, enddate]\
                    ), \
            )
#                            ~ Q(produsername='gangarbt')
#    jobList = QuerySetChain(\
#                    Jobsactive4.objects.filter(\
#                            produsername='gangarbt'
#                        ).filter(\
#                            modificationtime__range=[startdate, enddate]\
#                        ,
#                    ), \
#            )
##     jobList = QuerySetChain(\
##                     Jobsactive4.objects.filter(\
##                             jeditaskid=4000195
##                         ,
##                     ), \
##             )

    _logger.debug('|jobList|=' + str(jobList.count()))
    _logger.debug('jobList[:30]=' + str(jobList[:30]))
    jobList = sorted(jobList, key=lambda x:-x.pandaid)
    _logger.debug('jobList[:30]=' + str(jobList[:30]))
    if request.META.get('CONTENT_TYPE', 'text/plain') == 'text/plain':
        data = {
            'prefix': getPrefix(request),
            'jobList': jobList[:3000],
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


def jobInfoDefaultOrig(request):
        msg = 'Please provide prodUserName and ndays in your URL, e.g. http://pandawms.org/bigpandamon/job/info/<prodUserName>/<ndays>/'
        data = {
            'prefix': getPrefix(request), \
            'msg': msg \
        }
        data.update(getContextVariables(request))
        return render_to_response('pandajob/msg.html', data, RequestContext(request))


def jobInfoOrig(request, prodUserName, nhours=LAST_N_HOURS):
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


def jobInfoHoursOrig(request, prodUserName, nhours=LAST_N_HOURS):
    return jobInfo(request, prodUserName, nhours)


def jobInfoDaysOrig(request, prodUserName, nhours=LAST_N_DAYS * 24):
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
        jediJobsInTask -- view list of PanDA jobs in a dataTables table
                            data from API jedi/jobsintask
        
        :param request: Django's HTTP request 
        :type request: django.http.HttpRequest
        
    """
    reverseUrl = 'api-datatables-jedi-jobs-in-task'
    reverseUrlSmry = reverseUrl + '-smry'
    ### get URL prefix
    prefix = getPrefix(request)
    ### get reverse url of the data view
    dataUrl = reverse(reverseUrl)
    dataUrlSmry = reverse(reverseUrlSmry)
    ### get aoColumns pre-config
    aoColumns = []
    aoColumns += getAoColumnsDictWithTitles(COL_TITLES[reverseUrl])
    ### get filter fields
#    filterFields = ['fJtaskID']
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
    ### set request response data
    data = { \
            'prefix': prefix, \
            'datasrc': str(dataUrl + "?format=json"), \
            'datasrcsmry': str(dataUrlSmry + "?format=json"), \
            'columns': json_dumps(aoColumns), \
            'fieldIndices': json_dumps(fieldIndices), \
            'tableid_joblist': 'jediJobsInTask', \
            'tableid_joblist_smry': 'jediJobsInTask-smry', \
            'filterFields': filterFields, \
            'caption': 'jobs', \
    }
    data.update(getContextVariables(request))
    return render_to_response('pandajob/jedi/jobsintask.html', data, RequestContext(request))



#### new functionality backported from lsst
def setupView(request, opmode='', hours=0, limit=-99):
    global VOMODE
    global viewParams
    global LAST_N_HOURS_MAX, JOB_LIMIT
    global standard_fields
    print ':59 LAST_N_HOURS_MAX=', LAST_N_HOURS_MAX
    setupHomeCloud()
    settings.ENV['MON_VO'] = ''
    viewParams['MON_VO'] = ''
    VOMODE = ''
    for vo in VOLIST:
        if request.META['HTTP_HOST'].startswith(vo):
            VOMODE = vo
    ## If DB is Oracle, set vomode to atlas
#    if dbaccess['default']['ENGINE'].find('oracle') >= 0: VOMODE = 'atlas'
    if settings.DATABASES['default']['ENGINE'].find('oracle') >= 0: VOMODE = 'atlas'
    settings.ENV['MON_VO'] = VONAME[VOMODE]
    viewParams['MON_VO'] = settings.ENV['MON_VO']
    fields = standard_fields
    if VOMODE == 'atlas':
        LAST_N_HOURS_MAX = 12
        if 'hours' not in request.GET:
            JOB_LIMIT = 1000
        else:
            JOB_LIMIT = 1000
        if 'cloud' not in fields: fields.append('cloud')
        if 'atlasrelease' not in fields: fields.append('atlasrelease')
        if 'produsername' in request.GET or 'jeditaskid' in request.GET:
            if 'jobsetid' not in fields: fields.append('jobsetid')
            if 'hours' not in request.GET and ('jobsetid' in request.GET or 'taskid' in request.GET or 'jeditaskid' in request.GET):
                LAST_N_HOURS_MAX = 180 * 24
        else:
            if 'jobsetid' in fields: fields.remove('jobsetid')
    else:
        LAST_N_HOURS_MAX = 7 * 24
        JOB_LIMIT = 1000
    if hours > 0:
        ## Call param overrides default hours, but not a param on the URL
        LAST_N_HOURS_MAX = hours
    ## For site-specific queries, allow longer time window
    if 'computingsite' in request.GET:
        LAST_N_HOURS_MAX = 72
    ## hours specified in the URL takes priority over the above
    if 'hours' in request.GET:
        LAST_N_HOURS_MAX = int(request.GET['hours'])
    if limit != -99 and limit >= 0:
        ## Call param overrides default, but not a param on the URL
        JOB_LIMIT = limit
    if 'limit' in request.GET:
        JOB_LIMIT = int(request.GET['limit'])
    ## Exempt single-job, single-task etc queries from time constraint
    deepquery = False
    if 'jeditaskid' in request.GET: deepquery = True
    if 'taskid' in request.GET: deepquery = True
    if 'pandaid' in request.GET: deepquery = True
    if 'batchid' in request.GET: deepquery = True
    if deepquery:
        opmode = 'notime'
        LAST_N_HOURS_MAX = 24 * 365
    if opmode != 'notime':
        if LAST_N_HOURS_MAX <= 72 :
            viewParams['selection'] = ", last %s hours" % LAST_N_HOURS_MAX
        else:
            viewParams['selection'] = ", last %d days" % (float(LAST_N_HOURS_MAX) / 24.)
        if JOB_LIMIT < 100000 and JOB_LIMIT > 0:
            viewParams['selection'] += " (limit %s per table)" % JOB_LIMIT
        viewParams['selection'] += ". Query params: hours=%s" % LAST_N_HOURS_MAX
        if JOB_LIMIT < 100000 and JOB_LIMIT > 0:
            viewParams['selection'] += ", limit=%s" % JOB_LIMIT
    else:
        viewParams['selection'] = ""
    for param in request.GET:
        viewParams['selection'] += ", %s=%s " % (param, request.GET[param])
    print ':127 LAST_N_HOURS_MAX=', LAST_N_HOURS_MAX
    startdate = datetime.utcnow().replace(tzinfo=pytz.utc) - timedelta(hours=LAST_N_HOURS_MAX)
    startdate = startdate.strftime(defaultDatetimeFormat)
    enddate = datetime.utcnow().replace(tzinfo=pytz.utc).strftime(defaultDatetimeFormat)
    query = { 'modificationtime__range' : [startdate, enddate] }
    print ':134 query=', query
    ### Add any extensions to the query determined from the URL
    for vo in [ 'atlas', 'lsst' ]:
        if request.META['HTTP_HOST'].startswith(vo):
            query['vo'] = vo
    for param in request.GET:
        if param == 'cloud' and request.GET[param] == 'All': continue
        for field in Jobsactive4._meta.get_all_field_names():
            if param == field:
                if param == 'transformation' or param == 'transpath':
                    query['%s__endswith' % param] = request.GET[param]
                else:
                    query[param] = request.GET[param]
    if 'jobtype' in request.GET:
        jobtype = request.GET['jobtype']
    else:
        jobtype = opmode
    if jobtype == 'analysis':
        query['prodsourcelabel__in'] = ['panda', 'user']
    elif jobtype == 'production':
        query['prodsourcelabel'] = 'managed'
    elif jobtype == 'test':
        query['prodsourcelabel__contains'] = 'test'
    print ':157 query=', query
    return query



def jobSummaryDict(request, jobs, fieldlist=None):
    """ Return a dictionary summarizing the field values for the chosen most interesting fields """
    sumd = {}
    if fieldlist:
        flist = fieldlist
    else:
        flist = standard_fields
    for job in jobs:
        for f in flist:
            if job[f]:
                if f == 'taskid' and int(job[f]) < 1000000 and 'produsername' not in request.GET: continue
                if not f in sumd: sumd[f] = {}
                if not job[f] in sumd[f]: sumd[f][job[f]] = 0
                sumd[f][job[f]] += 1
        if job['specialhandling']:
            if not 'specialhandling' in sumd: sumd['specialhandling'] = {}
            shl = job['specialhandling'].split()
            for v in shl:
                if not v in sumd['specialhandling']: sumd['specialhandling'][v] = 0
                sumd['specialhandling'][v] += 1
    ## convert to ordered lists
    suml = []
    for f in sumd:
        itemd = {}
        itemd['field'] = f
        iteml = []
        kys = sumd[f].keys()
        kys.sort()
        for ky in kys:
            iteml.append({ 'kname' : ky, 'kvalue' : sumd[f][ky] })
        itemd['list'] = iteml
        suml.append(itemd)
    suml = sorted(suml, key=lambda x:x['field'])
    return suml


def taskSummaryDict(request, tasks, fieldlist=None):
    """ Return a dictionary summarizing the field values for the chosen most interesting fields """
    sumd = {}
    if fieldlist:
        flist = fieldlist
    else:
        flist = standard_taskfields
    for task in tasks:
        for f in flist:
            if task[f]:
                if not f in sumd: sumd[f] = {}
                if not task[f] in sumd[f]: sumd[f][task[f]] = 0
                sumd[f][task[f]] += 1
    ## convert to ordered lists
    suml = []
    for f in sumd:
        itemd = {}
        itemd['field'] = f
        iteml = []
        kys = sumd[f].keys()
        kys.sort()
        for ky in kys:
            iteml.append({ 'kname' : ky, 'kvalue' : sumd[f][ky] })
        itemd['list'] = iteml
        suml.append(itemd)
    suml = sorted(suml, key=lambda x:x['field'])
    return suml


def mainPage(request):
    setupView(request)
    if request.META.get('CONTENT_TYPE', 'text/plain') == 'text/plain':
        data = {
            'prefix': getPrefix(request),
            'viewParams' : viewParams,
        }
        data.update(getContextVariables(request))
        return render_to_response('pandajob/pandajob-mainPage.html', data, RequestContext(request))
    elif request.META.get('CONTENT_TYPE', 'text/plain') == 'application/json':
        return  HttpResponse('json', mimetype='text/html')
    else:
        return  HttpResponse('not understood', mimetype='text/html')


def extensibleURL(request):
    """ Return a URL that is ready for p=v query extension(s) to be appended """
    xurl = request.get_full_path()
    if xurl.endswith('/'): xurl = xurl[0:len(xurl) - 1]
    if xurl.find('?') > 0:
        xurl += '&'
    else:
        xurl += '?'
    if 'jobtype' in request.GET:
        xurl += "jobtype=%s&" % request.GET['jobtype']
    return xurl


def jobList(request, mode=None, param=None):
    query = setupView(request)
    print 'view:132 query=', query
    print 'view:133 JOB_LIMIT=', JOB_LIMIT
    jobs = []
    jobs.extend(Jobsdefined4.objects.filter(**query)[:JOB_LIMIT].values())
    jobs.extend(Jobsactive4.objects.filter(**query)[:JOB_LIMIT].values())
    jobs.extend(Jobswaiting4.objects.filter(**query)[:JOB_LIMIT].values())
    jobs.extend(Jobsarchived4.objects.filter(**query)[:JOB_LIMIT].values())
    jobs.extend(Jobsarchived.objects.filter(**query)[:JOB_LIMIT].values())

    ## If the list is for a particular JEDI task, filter out the jobs superseded by retries
    taskids = {}
    for job in jobs:
        if 'jeditaskid' in job: taskids[job['jeditaskid']] = 1
    droplist = []
    if len(taskids) == 1:
        for task in taskids:
            retryquery = {}
            retryquery['jeditaskid'] = task
            retries = JediJobRetryHistory.objects.filter(**retryquery).order_by('newpandaid').values()
        newjobs = []
        for job in jobs:
            dropJob = 0
            pandaid = job['pandaid']
            for retry in retries:
                if retry['oldpandaid'] == pandaid and retry['newpandaid'] != pandaid:
                    ## there is a retry for this job. Drop it.
                    print 'dropping', pandaid
                    dropJob = retry['newpandaid']
            if dropJob == 0:
                newjobs.append(job)
            else:
                droplist.append({ 'pandaid' : pandaid, 'newpandaid' : dropJob })
        droplist = sorted(droplist, key=lambda x:-x['pandaid'])
        jobs = newjobs

    jobs = cleanJobList(jobs)
    njobs = len(jobs)
    jobtype = ''
    if 'jobtype' in request.GET:
        jobtype = request.GET['jobtype']
    elif '/analysis' in request.path:
        jobtype = 'analysis'
    elif '/production' in request.path:
        jobtype = 'production'
#    tfirst = timezone.now()
    tfirst = datetime.utcnow().replace(tzinfo=pytz.utc)
    print 'tfirst=', tfirst
#    tlast = timezone.now() - timedelta(hours=2400)
    tlast = datetime.utcnow().replace(tzinfo=pytz.utc) - timedelta(hours=2400)
    print 'tlast=', tlast
    plow = 1000000
    phigh = -1000000
    for job in jobs:
        if job['modificationtime'] > tlast:
            tlast = job['modificationtime']
        if job['modificationtime'] < tfirst:
            tfirst = job['modificationtime']
        if job['currentpriority'] > phigh:
            phigh = job['currentpriority']
        if job['currentpriority'] < plow:
            plow = job['currentpriority']
    print 'views:217 tfirst=', tfirst
    print 'views:218 tlast=', tlast
    if request.META.get('CONTENT_TYPE', 'text/plain') == 'text/plain':
        sumd = jobSummaryDict(request, jobs)
        xurl = extensibleURL(request)
        data = {
            'prefix': getPrefix(request),
            'viewParams' : viewParams,
            'requestParams' : request.GET,
            'jobList': jobs,
            'jobtype' : jobtype,
            'njobs' : njobs,
            'user' : None,
            'sumd' : sumd,
            'xurl' : xurl,
            'droplist' : droplist,
            'ndrops' : len(droplist),
            'tfirst' : tfirst,
            'tlast' : tlast,
            'plow' : plow,
            'phigh' : phigh,
        }
        data.update(getContextVariables(request))
        return render_to_response('pandajob/jobList.html', data, RequestContext(request))
    elif request.META.get('CONTENT_TYPE', 'text/plain') == 'application/json':
        resp = []
        for job in jobs:
            resp.append({ 'pandaid': job.pandaid, 'status': job.jobstatus, 'prodsourcelabel': job.prodsourcelabel, 'produserid' : job.produserid})
        return  HttpResponse(json_dumps(resp), mimetype='text/html')


@csrf_exempt
def jobInfo(request, pandaid=None, batchid=None, p2=None, p3=None, p4=None):
    query = setupView(request, hours=365 * 24)
    jobid = '?'
    if pandaid:
        jobid = pandaid
        query['pandaid'] = pandaid
    if batchid:
        jobid = batchid
        query['batchid'] = batchid
    if 'pandaid' in request.GET:
        pandaid = request.GET['pandaid']
        jobid = pandaid
        query['pandaid'] = pandaid
    elif 'batchid' in request.GET:
        batchid = request.GET['batchid']
        jobid = "'" + batchid + "'"
        query['batchid'] = batchid
    startdate = datetime.utcnow().replace(tzinfo=pytz.utc) - timedelta(hours=LAST_N_HOURS_MAX)
    jobs = []
    jobs.extend(Jobsdefined4.objects.filter(**query).values())
    jobs.extend(Jobsactive4.objects.filter(**query).values())
    jobs.extend(Jobswaiting4.objects.filter(**query).values())
    jobs.extend(Jobsarchived4.objects.filter(**query).values())
    if len(jobs) == 0:
        jobs.extend(Jobsarchived.objects.filter(**query).values())

    jobs = cleanJobList(jobs, mode='nodrop')
    job = {}
    colnames = []
    columns = []
    try:
        job = jobs[0]
        colnames = job.keys()
        colnames.sort()
        for k in colnames:
            val = job[k]
            if job[k] == None:
                val = ''
                continue
            pair = { 'name' : k, 'value' : val }
            columns.append(pair)
    except IndexError:
        job = {}

    ## Check for logfile extracts
    logs = Logstable.objects.filter(pandaid=pandaid)
    if logs:
        logextract = logs[0].log1
    else:
        logextract = None

    ## Get job files
    files = []
    files.extend(Filestable4.objects.filter(pandaid=pandaid).order_by('type').values())
    if len(files) == 0:
        files.extend(FilestableArch.objects.filter(pandaid=pandaid).order_by('type').values())
    nfiles = len(files)
    logfile = {}
    for file in files:
        if file['type'] == 'log':
            logfile['lfn'] = file['lfn']
            logfile['guid'] = file['guid']
            logfile['site'] = file['destinationse']

    if 'pilotid' in job and job['pilotid'] is not None and job['pilotid'].startswith('http'):
        stdout = job['pilotid'].split('|')[0]
        stderr = stdout.replace('.out', '.err')
        stdlog = stdout.replace('.out', '.log')
    else:
        stdout = stderr = stdlog = None

    if 'transformation' in job and job['transformation'] is not None and job['transformation'].startswith('http'):
        job['transformation'] = "<a href='%s'>%s</a>" % (job['transformation'], job['transformation'].split('/')[-1])

    ## Get job parameters
    jobparamrec = Jobparamstable.objects.filter(pandaid=pandaid)
    jobparams = None
    try:
        if jobparamrec: jobparams = jobparamrec[0].jobparameters
    except IndexError:
        jobparams = None

    ## If this is a JEDI job, look for job retries
    if 'jeditaskid' in job and job['jeditaskid'] > 0:
        ## Look for retries of this job
        retryquery = {}
        retryquery['jeditaskid'] = job['jeditaskid']
        retryquery['oldpandaid'] = job['pandaid']
        retries = JediJobRetryHistory.objects.filter(**retryquery).order_by('newpandaid').reverse().values()
        ## Look for jobs for which this job is a retry
        pretryquery = {}
        pretryquery['jeditaskid'] = job['jeditaskid']
        pretryquery['newpandaid'] = job['pandaid']
        pretries = JediJobRetryHistory.objects.filter(**pretryquery).order_by('oldpandaid').reverse().values()
    else:
        retries = None
        pretries = None

    if isEventService(job):
        ## for ES jobs, pass the event table
        evtable = JediEvents.objects.filter(pandaid=job['pandaid']).values()
    else:
        evtable = None

    ## For LSST, pick up parameters from jobparams
    if VOMODE == 'lsst' or ('vo' in job and job['vo'] == 'lsst'):
        lsstData = {}
        if jobparams:
            lsstParams = re.match('.*PIPELINE_TASK\=([a-zA-Z0-9]+).*PIPELINE_PROCESSINSTANCE\=([0-9]+).*PIPELINE_STREAM\=([0-9\.]+)', jobparams)
            if lsstParams:
                lsstData['pipelinetask'] = lsstParams.group(1)
                lsstData['processinstance'] = lsstParams.group(2)
                lsstData['pipelinestream'] = lsstParams.group(3)
    else:
        lsstData = None

    if request.META.get('CONTENT_TYPE', 'text/plain') == 'text/plain':
        data = {
            'prefix': getPrefix(request),
            'viewParams' : viewParams,
            'pandaid': pandaid,
            'job': job,
            'columns' : columns,
            'files' : files,
            'nfiles' : nfiles,
            'logfile' : logfile,
            'stdout' : stdout,
            'stderr' : stderr,
            'stdlog' : stdlog,
            'jobparams' : jobparams,
            'jobid' : jobid,
            'lsstData' : lsstData,
            'logextract' : logextract,
            'retries' : retries,
            'pretries' : pretries,
            'eventservice' : isEventService(job),
            'evtable' : evtable,
        }
        data.update(getContextVariables(request))
        return render_to_response('pandajob/jobInfo.html', data, RequestContext(request))
    elif request.META.get('CONTENT_TYPE', 'text/plain') == 'application/json':
        return  HttpResponse('json', mimetype='text/html')
    else:
        return  HttpResponse('not understood', mimetype='text/html')


def userList(request):
    nhours = 90 * 24
    query = setupView(request, hours=nhours, limit=-99)
    if VOMODE == 'atlas':
        view = 'database'
    else:
        view = 'dynamic'
    if 'view' in request.GET:
        view = request.GET['view']
    sumd = []
    jobsumd = []
    userdb = []
    userdbl = []
    userstats = {}
    if view == 'database':
        startdate = datetime.utcnow().replace(tzinfo=pytz.utc) - timedelta(hours=nhours)
        startdate = startdate.strftime(defaultDatetimeFormat)
        enddate = datetime.utcnow().replace(tzinfo=pytz.utc).strftime(defaultDatetimeFormat)
        query = { 'latestjob__range' : [startdate, enddate] }
        #viewParams['selection'] = ", last %d days" % (float(nhours)/24.)
        ## Use the users table
        userdb = Users.objects.filter(**query).order_by('name')
        if 'sortby' in request.GET:
            sortby = request.GET['sortby']
            if sortby == 'name':
                userdb = Users.objects.filter(**query).order_by('name')
            elif sortby == 'njobs':
                userdb = Users.objects.filter(**query).order_by('njobsa').reverse()
            elif sortby == 'date':
                userdb = Users.objects.filter(**query).order_by('latestjob').reverse()
            elif sortby == 'cpua1':
                userdb = Users.objects.filter(**query).order_by('cpua1').reverse()
            elif sortby == 'cpua7':
                userdb = Users.objects.filter(**query).order_by('cpua7').reverse()
            elif sortby == 'cpup1':
                userdb = Users.objects.filter(**query).order_by('cpup1').reverse()
            elif sortby == 'cpup7':
                userdb = Users.objects.filter(**query).order_by('cpup7').reverse()
            else:
                userdb = Users.objects.filter(**query).order_by('name')
        else:
            userdb = Users.objects.filter(**query).order_by('name')

        anajobs = 0
        n1000 = 0
        n10k = 0
        nrecent3 = 0
        nrecent7 = 0
        nrecent30 = 0
        nrecent90 = 0
        ## Move to a list of dicts and adjust CPU unit
        for u in userdb:
            udict = {}
            udict['name'] = u.name
            udict['njobsa'] = u.njobsa
            if u.cpua1: udict['cpua1'] = "%0.1f" % (int(u.cpua1) / 3600.)
            if u.cpua7: udict['cpua7'] = "%0.1f" % (int(u.cpua7) / 3600.)
            if u.cpup1: udict['cpup1'] = "%0.1f" % (int(u.cpup1) / 3600.)
            if u.cpup7: udict['cpup7'] = "%0.1f" % (int(u.cpup7) / 3600.)
            udict['latestjob'] = u.latestjob
            userdbl.append(udict)

            if u.njobsa > 0: anajobs += u.njobsa
            if u.njobsa >= 1000: n1000 += 1
            if u.njobsa >= 10000: n10k += 1
            if u.latestjob != None:
#                latest = datetime.utcnow() - u.latestjob.replace(tzinfo=None)
                latest = datetime.utcnow().replace(tzinfo=pytz.utc) - u.latestjob.replace(tzinfo=pytz.utc)
                if latest.days < 4: nrecent3 += 1
                if latest.days < 8: nrecent7 += 1
                if latest.days < 31: nrecent30 += 1
                if latest.days < 91: nrecent90 += 1
        userstats['anajobs'] = anajobs
        userstats['n1000'] = n1000
        userstats['n10k'] = n10k
        userstats['nrecent3'] = nrecent3
        userstats['nrecent7'] = nrecent7
        userstats['nrecent30'] = nrecent30
        userstats['nrecent90'] = nrecent90
    else:
        if VOMODE == 'atlas':
            nhours = 12
        else:
            nhours = 7 * 24
        query = setupView(request, hours=nhours, limit=3000)
        ## dynamically assemble user summary info
        values = 'produsername', 'cloud', 'computingsite', 'cpuconsumptiontime', 'jobstatus', 'transformation', 'prodsourcelabel', 'specialhandling', 'vo', 'modificationtime', 'pandaid'
        jobs = QuerySetChain(\
                        Jobsdefined4.objects.filter(**query).order_by('-modificationtime')[:JOB_LIMIT].values(*values),
                        Jobsactive4.objects.filter(**query).order_by('-modificationtime')[:JOB_LIMIT].values(*values),
                        Jobswaiting4.objects.filter(**query).order_by('-modificationtime')[:JOB_LIMIT].values(*values),
                        Jobsarchived4.objects.filter(**query).order_by('-modificationtime')[:JOB_LIMIT].values(*values),
        )
        for job in jobs:
            if job['transformation']: job['transformation'] = job['transformation'].split('/')[-1]
        sumd = userSummaryDict(jobs)
        jobsumd = jobSummaryDict(request, jobs, [ 'jobstatus', 'prodsourcelabel', 'specialhandling', 'vo', 'transformation', ])
    if request.META.get('CONTENT_TYPE', 'text/plain') == 'text/plain':
        data = {
            'viewParams' : viewParams,
            'requestParams' : request.GET,
            'xurl' : extensibleURL(request),
            'url' : request.path,
            'sumd' : sumd,
            'jobsumd' : jobsumd,
            'userdb' : userdbl,
            'userstats' : userstats,
        }
        data.update(getContextVariables(request))
        return render_to_response('pandajob/userList.html', data, RequestContext(request))
    elif request.META.get('CONTENT_TYPE', 'text/plain') == 'application/json':
        resp = sumd
        return  HttpResponse(json_dumps(resp), mimetype='text/html')


def userInfo(request, user):
    query = setupView(request, hours=24, limit=300)
    query['produsername'] = user
    jobs = []
    values = 'produsername', 'cloud', 'computingsite', 'cpuconsumptiontime', 'jobstatus', 'transformation', 'prodsourcelabel', 'specialhandling', 'vo', 'modificationtime', 'pandaid', 'atlasrelease', 'jobsetid', 'processingtype', 'workinggroup', 'jeditaskid', 'taskid', 'currentpriority', 'creationtime', 'starttime', 'endtime', 'brokerageerrorcode', 'brokerageerrordiag', 'ddmerrorcode', 'ddmerrordiag', 'exeerrorcode', 'exeerrordiag', 'jobdispatchererrorcode', 'jobdispatchererrordiag', 'piloterrorcode', 'piloterrordiag', 'superrorcode', 'superrordiag', 'taskbuffererrorcode', 'taskbuffererrordiag', 'transexitcode'
    jobs.extend(Jobsdefined4.objects.filter(**query)[:JOB_LIMIT].values(*values))
    jobs.extend(Jobsactive4.objects.filter(**query)[:JOB_LIMIT].values(*values))
    jobs.extend(Jobswaiting4.objects.filter(**query)[:JOB_LIMIT].values(*values))
    jobs.extend(Jobsarchived4.objects.filter(**query)[:JOB_LIMIT].values(*values))
    if LAST_N_HOURS_MAX > 72: jobs.extend(Jobsarchived.objects.filter(**query)[:JOB_LIMIT].values(*values))
    jobs = cleanJobList(jobs)
    userdb = Users.objects.filter(name=user).values()
    if len(userdb) > 0:
        userstats = userdb[0]
        for field in ['cpua1', 'cpua7', 'cpup1', 'cpup7' ]:
            userstats[field] = "%0.1f" % (float(userstats[field]) / 3600.)
    else:
        userstats = None
#    tfirst = timezone.now()
    tfirst = datetime.utcnow().replace(tzinfo=pytz.utc)
    print 'tfirst=', tfirst
#    tlast = timezone.now() - timedelta(hours=2400)
    tlast = datetime.utcnow().replace(tzinfo=pytz.utc) - timedelta(hours=2400)
    print 'tlast=', tlast
    plow = 1000000
    phigh = -1000000
    for job in jobs:
        if job['modificationtime'] > tlast:
            tlast = job['modificationtime']
        if job['modificationtime'] < tfirst:
            tfirst = job['modificationtime']
        if job['currentpriority'] > phigh:
            phigh = job['currentpriority']
        if job['currentpriority'] < plow:
            plow = job['currentpriority']

    ## Divide up jobs by jobset and summarize
    jobsets = {}
    for job in jobs:
        if 'jobsetid' not in job or job['jobsetid'] == None: continue
        if job['jobsetid'] not in jobsets:
            jobsets[job['jobsetid']] = {}
            jobsets[job['jobsetid']]['jobsetid'] = job['jobsetid']
            jobsets[job['jobsetid']]['jobs'] = []
        jobsets[job['jobsetid']]['jobs'].append(job)
    for jobset in jobsets:
        jobsets[jobset]['sum'] = jobStateSummary(jobsets[jobset]['jobs'])
        jobsets[jobset]['njobs'] = len(jobsets[jobset]['jobs'])
#        tfirst = timezone.now()
        tfirst = datetime.utcnow().replace(tzinfo=pytz.utc)
        print 'tfirst=', tfirst
#        tlast = timezone.now() - timedelta(hours=2400)
        tlast = datetime.utcnow().replace(tzinfo=pytz.utc) - timedelta(hours=2400)
        print 'tlast=', tlast
        plow = 1000000
        phigh = -1000000
        for job in jobsets[jobset]['jobs']:
            if job['modificationtime'] > tlast: tlast = job['modificationtime']
            if job['modificationtime'] < tfirst: tfirst = job['modificationtime']
            if job['currentpriority'] > phigh: phigh = job['currentpriority']
            if job['currentpriority'] < plow: plow = job['currentpriority']
        jobsets[jobset]['tfirst'] = tfirst
        jobsets[jobset]['tlast'] = tlast
        jobsets[jobset]['plow'] = plow
        jobsets[jobset]['phigh'] = phigh
    jobsetl = []
    jsk = jobsets.keys()
    jsk.sort(reverse=True)
    for jobset in jsk:
        jobsetl.append(jobsets[jobset])

    if request.META.get('CONTENT_TYPE', 'text/plain') == 'text/plain':
        sumd = userSummaryDict(jobs)
        flist = [ 'jobstatus', 'prodsourcelabel', 'processingtype', 'specialhandling', 'transformation', 'jobsetid', 'taskid', 'jeditaskid', 'computingsite', 'cloud', 'workinggroup', ]
        if VOMODE != 'atlas':
            flist.append('vo')
        else:
            flist.append('atlasrelease')
        jobsumd = jobSummaryDict(request, jobs, flist)
        data = {
            'viewParams' : viewParams,
            'xurl' : extensibleURL(request),
            'user' : user,
            'sumd' : sumd,
            'jobsumd' : jobsumd,
            'jobList' : jobs,
            'query' : query,
            'userstats' : userstats,
            'tfirst' : tfirst,
            'tlast' : tlast,
            'plow' : plow,
            'phigh' : phigh,
            'jobsets' : jobsetl,
            'njobsets' : len(jobsetl),
        }
        data.update(getContextVariables(request))
        return render_to_response('pandajob/userInfo.html', data, RequestContext(request))
    elif request.META.get('CONTENT_TYPE', 'text/plain') == 'application/json':
        resp = sumd
        return  HttpResponse(json_dumps(resp), mimetype='text/html')


def siteList(request):
    setupView(request, opmode='notime')
    query = {}
    ### Add any extensions to the query determined from the URL
    if VOMODE == 'lsst': query['siteid__contains'] = 'LSST'
    prod = False
    for param in request.GET:
        if param == 'category' and request.GET[param] == 'multicloud':
            query['multicloud__isnull'] = False
        if param == 'category' and request.GET[param] == 'analysis':
            query['siteid__contains'] = 'ANALY'
        if param == 'category' and request.GET[param] == 'test':
            query['siteid__icontains'] = 'test'
        if param == 'category' and request.GET[param] == 'production':
            prod = True
        for field in Schedconfig._meta.get_all_field_names():
            if param == field:
                query[param] = request.GET[param]
    siteres = Schedconfig.objects.filter(**query).exclude(cloud='CMS').values()
    sites = []
    for site in siteres:
        if 'category' in request.GET and request.GET['category'] == 'multicloud':
            if (site['multicloud'] == 'None') or (not re.match('[A-Z]+', site['multicloud'])): continue
        sites.append(site)
    sites = sorted(sites, key=lambda x:x['nickname'])
    if prod:
        newsites = []
        for site in sites:
            if site['siteid'].find('ANALY') >= 0:
                pass
            elif site['siteid'].lower().find('test') >= 0:
                pass
            else:
                newsites.append(site)
        sites = newsites
    for site in sites:
        if site['maxtime'] and (site['maxtime'] > 0) : site['maxtime'] = "%.1f" % (float(site['maxtime']) / 3600.)
    if request.META.get('CONTENT_TYPE', 'text/plain') == 'text/plain':
        sumd = siteSummaryDict(sites)
        data = {
            'viewParams' : viewParams,
            'sites': sites,
            'sumd' : sumd,
            'xurl' : extensibleURL(request),
        }
        #data.update(getContextVariables(request))
        return render_to_response('pandajob/siteList.html', data, RequestContext(request))
    elif request.META.get('CONTENT_TYPE', 'text/plain') == 'application/json':
        resp = sites
        return  HttpResponse(json_dumps(resp), mimetype='text/html')


def siteInfo(request, site):
    setupView(request)
#    startdate = datetime.utcnow() - timedelta(hours=LAST_N_HOURS_MAX)
    startdate = datetime.utcnow().replace(tzinfo=pytz.utc) - timedelta(hours=LAST_N_HOURS_MAX)
    startdate = startdate.strftime(defaultDatetimeFormat)
#    enddate = datetime.utcnow().strftime(defaultDatetimeFormat)
    enddate = datetime.utcnow().replace(tzinfo=pytz.utc).strftime(defaultDatetimeFormat)
    query = {'siteid' : site}
    sites = Schedconfig.objects.filter(**query)
    colnames = []
    try:
        siterec = sites[0]
        colnames = siterec.get_all_fields()
    except IndexError:
        siterec = {}

    if request.META.get('CONTENT_TYPE', 'text/plain') == 'text/plain':
        attrs = []
        attrs.append({'name' : 'Status', 'value' : siterec.status })
        attrs.append({'name' : 'Comment', 'value' : siterec.comment_field })
        attrs.append({'name' : 'GOC name', 'value' : siterec.gocname })
        attrs.append({'name' : 'Cloud', 'value' : siterec.cloud })
        attrs.append({'name' : 'Tier', 'value' : siterec.tier })
        attrs.append({'name' : 'Maximum memory', 'value' : "%.1f GB" % (float(siterec.maxmemory) / 1000.) })
        attrs.append({'name' : 'Maximum time', 'value' : "%.1f hours" % (float(siterec.maxtime) / 3600.) })
        data = {
            'viewParams' : viewParams,
            'site' : siterec,
            'colnames' : colnames,
            'attrs' : attrs,
            'name' : site,
        }
        data.update(getContextVariables(request))
        return render_to_response('pandajob/siteInfo.html', data, RequestContext(request))
    elif request.META.get('CONTENT_TYPE', 'text/plain') == 'application/json':
        resp = []
        for job in jobList:
            resp.append({ 'pandaid': job.pandaid, 'status': job.jobstatus, 'prodsourcelabel': job.prodsourcelabel, 'produserid' : job.produserid})
        return  HttpResponse(json_dumps(resp), mimetype='text/html')


def dashboard(request, view=''):
#    if dbaccess['default']['ENGINE'].find('oracle') >= 0:
    if settings.DATABASES['default']['ENGINE'].find('oracle') >= 0:
        VOMODE = 'atlas'
    else:
        VOMODE = ''
    if VOMODE != 'atlas':
        hours = 24 * 7
    else:
        hours = 12
    query = setupView(request, hours=hours, limit=999999, opmode=view)

    if VOMODE != 'atlas':
        vosummarydata = voSummary(query)
        vos = {}
        for rec in vosummarydata:
            vo = rec['vo']
            #if vo == None: vo = 'Unassigned'
            if vo == None: continue
            jobstatus = rec['jobstatus']
            count = rec['jobstatus__count']
            if vo not in vos:
                vos[vo] = {}
                vos[vo]['name'] = vo
                vos[vo]['count'] = 0
                vos[vo]['states'] = {}
                vos[vo]['statelist'] = []
                for state in sitestatelist:
                    vos[vo]['states'][state] = {}
                    vos[vo]['states'][state]['name'] = state
                    vos[vo]['states'][state]['count'] = 0
            vos[vo]['count'] += count
            vos[vo]['states'][jobstatus]['count'] += count
        ## Convert dict to summary list
        vokeys = vos.keys()
        vokeys.sort()
        vosummary = []
        for vo in vokeys:
            for state in sitestatelist:
                vos[vo]['statelist'].append(vos[vo]['states'][state])
                if int(vos[vo]['states']['finished']['count']) + int(vos[vo]['states']['failed']['count']) > 0:
                    vos[vo]['pctfail'] = "%2d" % (100.*float(vos[vo]['states']['failed']['count']) / (vos[vo]['states']['finished']['count'] + vos[vo]['states']['failed']['count']))
                    if int(vos[vo]['pctfail']) > 5: vos[vo]['pctfail'] = "<font color=red>%s</font>" % vos[vo]['pctfail']
            vosummary.append(vos[vo])

    else:
        vosummary = []

    cloudview = 'cloud'
    if 'cloudview' in request.GET:
        cloudview = request.GET['cloudview']
    sitesummarydata = siteSummary(query)
    clouds = {}
    totstates = {}
    totjobs = 0
    for state in sitestatelist:
        totstates[state] = 0
    for rec in sitesummarydata:
        if cloudview == 'cloud':
            cloud = rec['cloud']
        elif cloudview == 'region':
            if rec['computingsite'] in homeCloud:
                cloud = homeCloud[rec['computingsite']]
            else:
                print "ERROR cloud not known", rec
        site = rec['computingsite']
        jobstatus = rec['jobstatus']
        count = rec['jobstatus__count']
        totjobs += count
        totstates[jobstatus] += count
        if cloud not in clouds:
            clouds[cloud] = {}
            clouds[cloud]['name'] = cloud
            clouds[cloud]['count'] = 0
            clouds[cloud]['sites'] = {}
            clouds[cloud]['states'] = {}
            clouds[cloud]['statelist'] = []
            for state in sitestatelist:
                clouds[cloud]['states'][state] = {}
                clouds[cloud]['states'][state]['name'] = state
                clouds[cloud]['states'][state]['count'] = 0
        clouds[cloud]['count'] += count
        clouds[cloud]['states'][jobstatus]['count'] += count
        if site not in clouds[cloud]['sites']:
            clouds[cloud]['sites'][site] = {}
            clouds[cloud]['sites'][site]['name'] = site
            clouds[cloud]['sites'][site]['count'] = 0
            clouds[cloud]['sites'][site]['states'] = {}
            for state in sitestatelist:
                clouds[cloud]['sites'][site]['states'][state] = {}
                clouds[cloud]['sites'][site]['states'][state]['name'] = state
                clouds[cloud]['sites'][site]['states'][state]['count'] = 0
        clouds[cloud]['sites'][site]['count'] += count
        clouds[cloud]['sites'][site]['states'][jobstatus]['count'] += count

    ## Convert dict to summary list
    cloudkeys = clouds.keys()
    cloudkeys.sort()
    fullsummary = []
    allstated = {}
    allstated['finished'] = allstated['failed'] = 0
    allclouds = {}
    allclouds['name'] = 'All'
    allclouds['count'] = totjobs
    allclouds['sites'] = {}
    allclouds['states'] = totstates
    allclouds['statelist'] = []
    for state in sitestatelist:
        allstate = {}
        allstate['name'] = state
        allstate['count'] = totstates[state]
        allstated[state] = totstates[state]
        allclouds['statelist'].append(allstate)
    if int(allstated['finished']) + int(allstated['failed']) > 0:
        allclouds['pctfail'] = "%2d" % (100.*float(allstated['failed']) / (allstated['finished'] + allstated['failed']))
        if int(allclouds['pctfail']) > 5: allclouds['pctfail'] = "<font color=red>%s</font>" % allclouds['pctfail']
    fullsummary.append(allclouds)
    for cloud in cloudkeys:
        for state in sitestatelist:
            clouds[cloud]['statelist'].append(clouds[cloud]['states'][state])
        sites = clouds[cloud]['sites']
        sitekeys = sites.keys()
        sitekeys.sort()
        cloudsummary = []
        for site in sitekeys:
            sitesummary = []
            for state in sitestatelist:
                sitesummary.append(sites[site]['states'][state])
            sites[site]['summary'] = sitesummary
            if sites[site]['states']['finished']['count'] + sites[site]['states']['failed']['count'] > 0:
                sites[site]['pctfail'] = "%2d" % (100.*float(sites[site]['states']['failed']['count']) / (sites[site]['states']['finished']['count'] + sites[site]['states']['failed']['count']))
                if int(sites[site]['pctfail']) > 5: sites[site]['pctfail'] = "<font color=red>%s</font>" % sites[site]['pctfail']

            cloudsummary.append(sites[site])
        clouds[cloud]['summary'] = cloudsummary
        if clouds[cloud]['states']['finished']['count'] + clouds[cloud]['states']['failed']['count'] > 0:
            clouds[cloud]['pctfail'] = "%2d" % (100.*float(clouds[cloud]['states']['failed']['count']) / (clouds[cloud]['states']['finished']['count'] + clouds[cloud]['states']['failed']['count']))
            if int(clouds[cloud]['pctfail']) > 5: clouds[cloud]['pctfail'] = "<font color=red>%s</font>" % clouds[cloud]['pctfail']

        fullsummary.append(clouds[cloud])

    if request.META.get('CONTENT_TYPE', 'text/plain') == 'text/plain':
        xurl = extensibleURL(request)
        data = {
            'viewParams' : viewParams,
            'url' : request.path,
            'xurl' : xurl,
            'user' : None,
            'summary' : fullsummary,
            'vosummary' : vosummary,
            'view' : view,
            'cloudview': cloudview,
            'hours' : hours,
        }
        #data.update(getContextVariables(request))
        return render_to_response('pandajob/dashboard.html', data, RequestContext(request))
    elif request.META.get('CONTENT_TYPE', 'text/plain') == 'application/json':
        resp = []
        return  HttpResponse(json_dumps(resp), mimetype='text/html')


def dashAnalysis(request):
    return dashboard(request, view='analysis')


def dashProduction(request):
    return dashboard(request, view='production')


#class QuicksearchForm(forms.Form):
#    fieldName = forms.CharField(max_length=100)


def taskList(request):
    query = setupView(request, hours=180 * 24, limit=9999999)
    for param in request.GET:
#         if param == 'category' and request.GET[param] == 'multicloud':
#             query['multicloud__isnull'] = False
#         if param == 'category' and request.GET[param] == 'analysis':
#             query['siteid__contains'] = 'ANALY'
#         if param == 'category' and request.GET[param] == 'test':
#             query['siteid__icontains'] = 'test'
#         if param == 'category' and request.GET[param] == 'production':
#             prod = True
        for field in JediTasks._meta.get_all_field_names():
            if param == field:
                if param == 'transpath':
                    query['%s__endswith' % param] = request.GET[param]
                else:
                    query[param] = request.GET[param]
    tasks = JediTasks.objects.filter(**query).values()
    tasks = cleanTaskList(tasks)
    tasks = sorted(tasks, key=lambda x:-x['jeditaskid'])
    if request.META.get('CONTENT_TYPE', 'text/plain') == 'text/plain':
        sumd = taskSummaryDict(request, tasks)
        data = {
            'viewParams' : viewParams,
            'requestParams' : request.GET,
            'tasks': tasks,
            'sumd' : sumd,
            'xurl' : extensibleURL(request),
        }
        return render_to_response('pandajob/taskList.html', data, RequestContext(request))
    elif request.META.get('CONTENT_TYPE', 'text/plain') == 'application/json':
        resp = sites
        return  HttpResponse(json_dumps(resp), mimetype='text/html')


def taskInfo(request, jeditaskid=0):
    if 'jeditaskid' in request.GET:
        jeditaskid = request.GET['jeditaskid']
    setupView(request)
    query = {'jeditaskid' : jeditaskid}
    jobsummary = jobSummary2(query)
    tasks = JediTasks.objects.filter(**query).values()
    colnames = []
    columns = []
    try:
        taskrec = tasks[0]
        colnames = taskrec.keys()
        colnames.sort()
        for k in colnames:
            val = taskrec[k]
            if taskrec[k] == None:
                val = ''
                continue
            pair = { 'name' : k, 'value' : val }
            columns.append(pair)
    except IndexError:
        taskrec = None
    taskpars = JediTaskparams.objects.filter(**query).values()
    if len(taskpars) > 0:
        taskparams = taskpars[0]['taskparams']
        taskparams = json.loads(taskparams)
        tpkeys = taskparams.keys()
        tpkeys.sort()
        taskparaml = []
        for k in tpkeys:
            rec = { 'name' : k, 'value' : taskparams[k] }
            taskparaml.append(rec)
    else:
        taskparams = None
        taskparaml = None

    if request.META.get('CONTENT_TYPE', 'text/plain') == 'text/plain':
        attrs = []
        attrs.append({'name' : 'Status', 'value' : taskrec['status'] })
        data = {
            'viewParams' : viewParams,
            'task' : taskrec,
            'taskparams' : taskparams,
            'taskparaml' : taskparaml,
            'columns' : columns,
            'attrs' : attrs,
            'jobsummary' : jobsummary,
            'jeditaskid' : jeditaskid,
        }
        data.update(getContextVariables(request))
        return render_to_response('pandajob/taskInfo.html', data, RequestContext(request))
    elif request.META.get('CONTENT_TYPE', 'text/plain') == 'application/json':
        resp = []
        return  HttpResponse(json_dumps(resp), mimetype='text/html')


