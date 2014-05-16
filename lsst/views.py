import logging
from datetime import datetime, timedelta

from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.template import RequestContext, loader

from core.common.utils import getPrefix, getContextVariables, QuerySetChain
from core.common.settings import STATIC_URL, FILTER_UI_ENV, defaultDatetimeFormat
from core.pandajob.models import PandaJob, Jobsactive4, Jobsdefined4, Jobswaiting4, Jobsarchived4
from core.resource.models import Schedconfig
from core.common.settings.config import ENV

_logger = logging.getLogger('bigpandamon')
viewParams = {}

LAST_N_DAYS_MAX = 60

fields = [ 'computingsite', 'destinationse', 'jobstatus', 'prodsourcelabel', 'produsername', 'jeditaskid', 'transformation', 'vo', ]
sitefields = [ 'region', 'cloud', 'gocname', 'status', 'tier' ]

VOLIST = [ 'atlas', 'bigpanda', 'htcondor', 'lsst', ]
VONAME = { 'atlas' : 'ATLAS', 'bigpanda' : 'BigPanDA', 'htcondor' : 'HTCondor', 'lsst' : 'LSST', }
VOMODE = ' '

def setupView(request, mode=''):
    global VOMODE
    global viewParams
    global LAST_N_DAYS_MAX
    ENV['MON_VO'] = ''
    for vo in VOLIST:
        if request.META['HTTP_HOST'].startswith(vo):
            VOMODE = vo
            ENV['MON_VO'] = VONAME[vo]
    viewParams['MON_VO'] = ENV['MON_VO']
    if VOMODE == 'atlas':
        global LAST_N_DAYS_MAX
        LAST_N_DAYS_MAX = 3
    if mode != 'notime':
        viewParams['selection'] = " for the last %s days" % LAST_N_DAYS_MAX
    else:
        viewParams['selection'] = ""
    for param in request.GET:
        viewParams['selection'] += ", %s=%s " % ( param, request.GET[param] )

def jobSummaryDict(jobs):
    """ Return a dictionary summarizing the field values for the chosen most interesting fields """
    sumd = {}
    for job in jobs:
        for f in fields:
            if job[f]:
                if not f in sumd: sumd[f] = {}
                if not job[f] in sumd[f]: sumd[f][job[f]] = 0
                sumd[f][job[f]] += 1
        if job['specialhandling']:
            if not 'specialhandling' in sumd: sumd['specialhandling'] = {}
            shl = job['specialhandling'].split()
            for v in shl:
                if not v in sumd['specialhandling']: sumd['specialhandling'][v] = 0
                sumd['specialhandling'][v] += 1
    return sumd

def siteSummaryDict(sites):
    """ Return a dictionary summarizing the field values for the chosen most interesting fields """
    sumd = {}
    sumd['category'] = {}
    sumd['category']['test'] = 0
    sumd['category']['production'] = 0
    sumd['category']['analysis'] = 0
    sumd['category']['multicloud'] = 0
    for site in sites:
        for f in sitefields:
            if f in site:
                if not f in sumd: sumd[f] = {}
                if not site[f] in sumd[f]: sumd[f][site[f]] = 0
                sumd[f][site[f]] += 1
        isProd = True
        if site['siteid'].find('ANALY') >= 0:
            isProd = False
            sumd['category']['analysis'] += 1
        if site['siteid'].lower().find('test') >= 0:
            isProd = False
            sumd['category']['test'] += 1
        if site['multicloud'] != None and site['multicloud'] != 'None' and len(site['multicloud']) > 0:
            sumd['category']['multicloud'] += 1
        if isProd: sumd['category']['production'] += 1
    return sumd

def userSummaryDict(jobs):
    """ Return a dictionary summarizing the field values for the chosen most interesting fields """
    statelist = [ 'defined', 'waiting', 'assigned', 'activated', 'sent', 'running', 'holding', 'finished', 'failed', 'cancelled', ]
    sumd = {}
    for job in jobs:
        user = job['produsername']
        if not user in sumd:
            sumd[user] = {}
            for state in statelist:
                sumd[user][state] = 0
            sumd[user]['cputime'] = 0
            sumd[user]['njobs'] = 0
            for state in statelist:
                sumd[user]['n'+state] = 0
            sumd[user]['nsites'] = 0
            sumd[user]['sites'] = {}
            sumd[user]['nclouds'] = 0
            sumd[user]['clouds'] = {}
            sumd[user]['nqueued'] = 0
        cloud = job['cloud']
        site = job['computingsite']
        cpu = job['cpuconsumptiontime']
        state = job['jobstatus']
        sumd[user]['cputime'] += cpu
        sumd[user]['njobs'] += 1
        sumd[user]['n'+state] += 1
        if not site in sumd[user]['sites']: sumd[user]['sites'][site] = 0
        sumd[user]['sites'][site] += 1
        if not site in sumd[user]['clouds']: sumd[user]['clouds'][cloud] = 0
        sumd[user]['clouds'][cloud] += 1
    for user in sumd:
        sumd[user]['nsites'] = len(sumd[user]['sites'])
        sumd[user]['nclouds'] = len(sumd[user]['clouds'])
        sumd[user]['nqueued'] = sumd[user]['ndefined'] + sumd[user]['nwaiting'] + sumd[user]['nassigned'] + sumd[user]['nactivated']
    return sumd

def extensibleURL(request):
    """ Return a URL that is ready for p=v query extension(s) to be appended """
    xurl = request.get_full_path()
    if xurl.find('?') > 0:
        xurl += '&'
    else:
        xurl += '?'
    return xurl

def mainPage(request):
    setupView(request)
    if request.META.get('CONTENT_TYPE', 'text/plain') == 'text/plain':
        data = {
            'prefix': getPrefix(request),
            'viewParams' : viewParams,
        }
        data.update(getContextVariables(request))
        return render_to_response('lsst-mainPage.html', data, RequestContext(request))
    elif request.META.get('CONTENT_TYPE', 'text/plain') == 'application/json':
        return  HttpResponse('json', mimetype='text/html')
    else:
        return  HttpResponse('not understood', mimetype='text/html')

def jobList(request, mode=None, param=None):
    setupView(request)
    startdate = datetime.utcnow() - timedelta(days=LAST_N_DAYS_MAX)
    startdate = startdate.strftime(defaultDatetimeFormat)
    enddate = datetime.utcnow().strftime(defaultDatetimeFormat)
    query = { 'modificationtime__range' : [startdate, enddate] }
    ### Add any extensions to the query determined from the URL
    for vo in [ 'atlas', 'lsst' ]:
        if request.META['HTTP_HOST'].startswith(vo):
            query['vo'] = vo   
    for param in request.GET:
        for field in fields:
            if param == field:
                query[param] = request.GET[param]
    jobList = QuerySetChain(\
                    Jobsdefined4.objects.filter(**query),
                    Jobsactive4.objects.filter(**query),
                    Jobswaiting4.objects.filter(**query),
                    Jobsarchived4.objects.filter(**query),
            )

    jobList = sorted(jobList, key=lambda x:-x.pandaid)
    _logger.debug('jobList[:30]=' + str(jobList[:30]))
    if request.META.get('CONTENT_TYPE', 'text/plain') == 'text/plain':
        sumd = jobSummaryDict(jobList)
        xurl = extensibleURL(request)
        data = {
            'prefix': getPrefix(request),
            'viewParams' : viewParams,
            'jobList': jobList[:3000],
            'user' : None,
            'sumd' : sumd,
            'xurl' : xurl,
        }
        data.update(getContextVariables(request))
        return render_to_response('jobList.html', data, RequestContext(request))
    elif request.META.get('CONTENT_TYPE', 'text/plain') == 'application/json':
        resp = []
        for job in jobList:
            resp.append({ 'pandaid': job.pandaid, 'status': job.jobstatus, 'prodsourcelabel': job.prodsourcelabel, 'produserid' : job.produserid})
        return  HttpResponse(json_dumps(resp), mimetype='text/html')

def jobInfo(request, pandaid, p2=None, p3=None, p4=None):
    setupView(request)
    startdate = datetime.utcnow() - timedelta(days=LAST_N_DAYS_MAX)
    jobs = QuerySetChain(\
        Jobsdefined4.objects.filter(pandaid=pandaid), \
        Jobsactive4.objects.filter(pandaid=pandaid), \
        Jobswaiting4.objects.filter(pandaid=pandaid), \
        Jobsarchived4.objects.filter(pandaid=pandaid), \
    )
    jobs = sorted(jobs, key=lambda x:-x.pandaid)
    job = {}
    colnames = []
    try:
        job = jobs[0]
        colnames = job.get_all_fields()
    except IndexError:
        job = {}

    if request.META.get('CONTENT_TYPE', 'text/plain') == 'text/plain':
        data = {
            'prefix': getPrefix(request),
            'viewParams' : viewParams,
            'pandaid': pandaid,
            'job': job,
            'colnames' : colnames,
        }
        data.update(getContextVariables(request))
        return render_to_response('jobInfo.html', data, RequestContext(request))
    elif request.META.get('CONTENT_TYPE', 'text/plain') == 'application/json':
        return  HttpResponse('json', mimetype='text/html')
    else:
        return  HttpResponse('not understood', mimetype='text/html')

def userList(request):
    setupView(request)
    startdate = datetime.utcnow() - timedelta(days=LAST_N_DAYS_MAX)
    startdate = startdate.strftime(defaultDatetimeFormat)
    enddate = datetime.utcnow().strftime(defaultDatetimeFormat)
    query = { 'modificationtime__range' : [startdate, enddate] }
    ### Add any extensions to the query determined from the URL  
    if VOMODE == 'lsst': query['vo'] = 'lsst'
    if VOMODE == 'atlas': query['vo'] = 'atlas'
    jobs = QuerySetChain(\
                    Jobsdefined4.objects.filter(**query),
                    Jobsactive4.objects.filter(**query),
                    Jobswaiting4.objects.filter(**query),
                    Jobsarchived4.objects.filter(**query),
    )
    if request.META.get('CONTENT_TYPE', 'text/plain') == 'text/plain':
        sumd = userSummaryDict(jobs)
        data = {
            'viewParams' : viewParams,
            'xurl' : extensibleURL(request),
            'sumd' : sumd,
        }
        data.update(getContextVariables(request))
        return render_to_response('userList.html', data, RequestContext(request))
    elif request.META.get('CONTENT_TYPE', 'text/plain') == 'application/json':
        resp = sumd
        return  HttpResponse(json_dumps(resp), mimetype='text/html')

def userInfo(request, user):
    setupView(request)
    startdate = datetime.utcnow() - timedelta(days=LAST_N_DAYS_MAX)
    startdate = startdate.strftime(defaultDatetimeFormat)
    enddate = datetime.utcnow().strftime(defaultDatetimeFormat)
    query = { 'modificationtime__range' : [startdate, enddate], 'produsername' : user}
    ### Add any extensions to the query determined from the URL  
    if VOMODE == 'lsst': query['vo'] = 'lsst'
    if VOMODE == 'atlas': query['vo'] = 'atlas'
    for param in request.GET:
        for field in fields:
            if param == field:
                query[param] = request.GET[param]
    jobs = QuerySetChain(\
                    Jobsdefined4.objects.filter(**query),
                    Jobsactive4.objects.filter(**query),
                    Jobswaiting4.objects.filter(**query),
                    Jobsarchived4.objects.filter(**query),
    )
    jobs = sorted(jobs, key=lambda x:-x.pandaid)
    if request.META.get('CONTENT_TYPE', 'text/plain') == 'text/plain':
        sumd = userSummaryDict(jobs)
        jobsumd = jobSummaryDict(jobs)
        data = {
            'viewParams' : viewParams,
            'xurl' : extensibleURL(request),
            'user' : user,
            'sumd' : sumd,
            'jobsumd' : jobsumd,
            'jobList' : jobs,
        }
        data.update(getContextVariables(request))
        return render_to_response('userInfo.html', data, RequestContext(request))
    elif request.META.get('CONTENT_TYPE', 'text/plain') == 'application/json':
        resp = sumd
        return  HttpResponse(json_dumps(resp), mimetype='text/html')

def siteList(request):
    setupView(request, 'notime')
    query = {}
    ### Add any extensions to the query determined from the URL  
    if VOMODE == 'lsst': query['siteid__contains'] = 'LSST'
    prod = False
    for param in request.GET:
        if param == 'category' and request.GET[param] == 'multicloud':
            query['multicloud__isnull'] = 'False'
        if param == 'category' and request.GET[param] == 'analysis':
            query['siteid__contains'] = 'ANALY'
        if param == 'category' and request.GET[param] == 'test':
            query['siteid__icontains'] = 'test'
        if param == 'category' and request.GET[param] == 'production':
            prod = True
        for field in sitefields:
            if param == field:
                query[param] = request.GET[param]
    sites = []
    sites.extend(Schedconfig.objects.filter(**query).values())
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
    if request.META.get('CONTENT_TYPE', 'text/plain') == 'text/plain':
        sumd = siteSummaryDict(sites)
        data = {
            'viewParams' : viewParams,
            'sites': sites,
            'sumd' : sumd,
            'xurl' : extensibleURL(request),
        }
        data.update(getContextVariables(request))
        return render_to_response('siteList.html', data, RequestContext(request))
    elif request.META.get('CONTENT_TYPE', 'text/plain') == 'application/json':
        resp = sites
        return  HttpResponse(json_dumps(resp), mimetype='text/html')

def siteInfo(request, site):
    setupView(request)
    startdate = datetime.utcnow() - timedelta(days=LAST_N_DAYS_MAX)
    startdate = startdate.strftime(defaultDatetimeFormat)
    enddate = datetime.utcnow().strftime(defaultDatetimeFormat)
    query = {'siteid' : site}
    sites = Schedconfig.objects.filter(**query)
    colnames = []
    try:
        site = sites[0]
        colnames = site.get_all_fields()
    except IndexError:
        site = {}

    if request.META.get('CONTENT_TYPE', 'text/plain') == 'text/plain':
        data = {
            'viewParams' : viewParams,
            'site' : site,
            'colnames' : colnames,
        }
        data.update(getContextVariables(request))
        return render_to_response('siteInfo.html', data, RequestContext(request))
    elif request.META.get('CONTENT_TYPE', 'text/plain') == 'application/json':
        resp = []
        for job in jobList:
            resp.append({ 'pandaid': job.pandaid, 'status': job.jobstatus, 'prodsourcelabel': job.prodsourcelabel, 'produserid' : job.produserid})
        return  HttpResponse(json_dumps(resp), mimetype='text/html')
