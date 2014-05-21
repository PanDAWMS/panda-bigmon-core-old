import logging
from datetime import datetime, timedelta

from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.template import RequestContext, loader

from core.common.utils import getPrefix, getContextVariables, QuerySetChain
from core.common.settings import STATIC_URL, FILTER_UI_ENV, defaultDatetimeFormat
from core.pandajob.models import PandaJob, Jobsactive4, Jobsdefined4, Jobswaiting4, Jobsarchived4
from core.resource.models import Schedconfig
from core.common.models import Filestable4 
from core.common.models import Users
from core.common.settings.config import ENV

from settings.local import dbaccess

_logger = logging.getLogger('bigpandamon')
viewParams = {}

LAST_N_HOURS_MAX = 0
JOB_LIMIT = 0

fields = [ 'processingtype', 'computingsite', 'cloud', 'destinationse', 'jobstatus', 'prodsourcelabel', 'produsername', 'jeditaskid', 'taskid', 'transformation', 'vo', ]
sitefields = [ 'region', 'cloud', 'gocname', 'status', 'tier', 'comment_field' ]

VOLIST = [ 'atlas', 'bigpanda', 'htcondor', 'lsst', ]
VONAME = { 'atlas' : 'ATLAS', 'bigpanda' : 'BigPanDA', 'htcondor' : 'HTCondor', 'lsst' : 'LSST', '' : '' }
VOMODE = ' '

def setupView(request, mode='', hours=0):
    global VOMODE
    global viewParams
    global LAST_N_HOURS_MAX, JOB_LIMIT
    ENV['MON_VO'] = ''
    viewParams['MON_VO'] = ''
    VOMODE = ''
    for vo in VOLIST:
        if request.META['HTTP_HOST'].startswith(vo):
            VOMODE = vo
    ## If DB is Oracle, set vomode to atlas
    if dbaccess['default']['ENGINE'].find('oracle') >= 0: VOMODE = 'atlas'
    ENV['MON_VO'] = VONAME[VOMODE]
    viewParams['MON_VO'] = ENV['MON_VO']
    if VOMODE == 'atlas':
        LAST_N_HOURS_MAX = 12
        JOB_LIMIT = 500
    else:
        LAST_N_HOURS_MAX = 30*24
        JOB_LIMIT = 3000
    if hours > 0:
        ## Call param overrides default hours, but not a param on the URL
        LAST_N_HOURS_MAX = max(LAST_N_HOURS_MAX, hours)
    if 'hours' in request.GET:
        LAST_N_HOURS_MAX = int(request.GET['hours'])
    if 'limit' in request.GET:
        JOB_LIMIT = int(request.GET['limit'])
    ## For site-specific queries, allow longer time window
    if 'computingsite' in request.GET:
        LAST_N_HOURS_MAX = 72
    if mode != 'notime':
        if LAST_N_HOURS_MAX <= 48 :
            viewParams['selection'] = ", last %s hours" % LAST_N_HOURS_MAX
        else:
            viewParams['selection'] = ", last %.1f days" % (float(LAST_N_HOURS_MAX)/24.)
        if JOB_LIMIT < 1000:
            viewParams['selection'] += " (limit %s per table)" % JOB_LIMIT
        viewParams['selection'] += ". Query params: hours=%s, limit=%s" % ( LAST_N_HOURS_MAX, JOB_LIMIT )
    else:
        viewParams['selection'] = ""
    for param in request.GET:
        viewParams['selection'] += ", %s=%s " % ( param, request.GET[param] )
    startdate = datetime.utcnow() - timedelta(hours=LAST_N_HOURS_MAX)
    startdate = startdate.strftime(defaultDatetimeFormat)
    enddate = datetime.utcnow().strftime(defaultDatetimeFormat)
    query = { 'modificationtime__range' : [startdate, enddate] }
    ### Add any extensions to the query determined from the URL
    for vo in [ 'atlas', 'lsst' ]:
        if request.META['HTTP_HOST'].startswith(vo):
            query['vo'] = vo   
    for param in request.GET:
        for field in Jobsactive4._meta.get_all_field_names():
            if param == field:
                if param == 'transformation':
                    query['%s__endswith' % param] = request.GET[param]
                else:
                    query[param] = request.GET[param]
    if 'jobtype' in request.GET:
        import operator
        if request.GET['jobtype'] == 'analysis':
            query['prodsourcelabel__in'] = ['panda', 'user']
        elif request.GET['jobtype'] == 'production':
            query['prodsourcelabel'] = 'managed'
        elif request.GET['jobtype'] == 'test':
            query['prodsourcelabel'] = 'test'
    return query

def jobSummaryDict(jobs, fieldlist = None):
    """ Return a dictionary summarizing the field values for the chosen most interesting fields """
    sumd = {}
    if fieldlist:
        flist = fieldlist
    else:
        flist = fields
    for job in jobs:
        for f in flist:
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
    return suml

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
    return suml

def userSummaryDict(jobs):
    """ Return a dictionary summarizing the field values for the chosen most interesting fields """
    statelist = [ 'defined', 'waiting', 'assigned', 'activated', 'sent', 'running', 'holding', 'finished', 'failed', 'cancelled', 'transferring', 'starting', 'pending' ]
    sumd = {}
    for job in jobs:
        user = job['produsername'].lower()
        if not user in sumd:
            sumd[user] = {}
            for state in statelist:
                sumd[user][state] = 0
            sumd[user]['name'] = job['produsername']
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
        cpu = float(job['cpuconsumptiontime'])/1.
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
        sumd[user]['cputime'] = "%d" % float(sumd[user]['cputime'])
    ## convert to list ordered by username
    ukeys = sumd.keys()
    ukeys.sort()
    suml = []
    for u in ukeys:
        uitem = {}
        uitem['name'] = u
        uitem['dict'] = sumd[u]
        suml.append(uitem)
    return suml

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

def errorInfo(job):
    errtxt = ''
    if int(job['brokerageerrorcode']) != 0:
        errtxt += 'Brokerage error %s: %s <br>' % ( job['brokerageerrorcode'], job['brokerageerrordiag'] )
    if int(job['ddmerrorcode']) != 0:
        errtxt += 'DDM error %s: %s <br>' % ( job['ddmerrorcode'], job['ddmerrordiag'] )
    if int(job['exeerrorcode']) != 0:
        errtxt += 'Executable error %s: %s <br>' % ( job['exeerrorcode'], job['exeerrordiag'] )
    if int(job['jobdispatchererrorcode']) != 0:
        errtxt += 'Dispatcher error %s: %s <br>' % ( job['jobdispatchererrorcode'], job['jobdispatchererrordiag'] )
    if int(job['piloterrorcode']) != 0:
        errtxt += 'Pilot error %s: %s <br>' % ( job['piloterrorcode'], job['piloterrordiag'] )
    if int(job['superrorcode']) != 0:
        errtxt += 'Sup error %s: %s <br>' % ( job['superrorcode'], job['superrordiag'] )
    if int(job['taskbuffererrorcode']) != 0:
        errtxt += 'Task buffer error %s: %s <br>' % ( job['taskbuffererrorcode'], job['taskbuffererrordiag'] )
    if job['transexitcode'] != '' and int(job['transexitcode']) > 0:
        errtxt += 'Payload transformation exit code %s' % job['transexitcode']
    return errtxt

def jobList(request, mode=None, param=None):
    query = setupView(request)
    jobList = QuerySetChain(\
                    Jobsdefined4.objects.filter(**query).order_by('-modificationtime')[:JOB_LIMIT].values(),
                    Jobsactive4.objects.filter(**query).order_by('-modificationtime')[:JOB_LIMIT].values(),
                    Jobswaiting4.objects.filter(**query).order_by('-modificationtime')[:JOB_LIMIT].values(),
                    Jobsarchived4.objects.filter(**query).order_by('-modificationtime')[:JOB_LIMIT].values(),
            )

    jobList = sorted(jobList, key=lambda x:-x['pandaid'])
    for job in jobList:
        if job['transformation']: job['transformation'] = job['transformation'].split('/')[-1]
        if job['jobstatus'] == 'failed':
            job['errorinfo'] = errorInfo(job)
        else:
            job['errorinfo'] = ''
    if request.META.get('CONTENT_TYPE', 'text/plain') == 'text/plain':
        sumd = jobSummaryDict(jobList)
        xurl = extensibleURL(request)
        data = {
            'prefix': getPrefix(request),
            'viewParams' : viewParams,
            'jobList': jobList,
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
    startdate = datetime.utcnow() - timedelta(hours=LAST_N_HOURS_MAX)
    jobs = QuerySetChain(\
        Jobsdefined4.objects.filter(pandaid=pandaid).values(), \
        Jobsactive4.objects.filter(pandaid=pandaid).values(), \
        Jobswaiting4.objects.filter(pandaid=pandaid).values(), \
        Jobsarchived4.objects.filter(pandaid=pandaid).values(), \
    )
    jobs = sorted(jobs, key=lambda x:-x['pandaid'])
    job = {}
    colnames = []
    try:
        job = jobs[0]
        colnames = job.keys()
        colnames.sort()
        columns = []
        for k in colnames:
            val = job[k]
            if job[k] == None:
                val = ''
                continue
            pair = { 'name' : k, 'value' : val }
            columns.append(pair)
    except IndexError:
        job = {}

    files = Filestable4.objects.filter(pandaid=pandaid).values() 
    nfiles = len(files)
    logfile = {} 
    for file in files:
        if file['type'] == 'log': 
            logfile['lfn'] = file['lfn'] 
            logfile['guid'] = file['guid'] 
            logfile['site'] = file['destinationse'] 

    if 'pilotid' in job and job['pilotid'] is not None and job['pilotid'].startswith('http'):
        stdout = job['pilotid'].split('|')[0]
        stderr = stdout.replace('.out','.err')
        stdlog = stdout.replace('.out','.log')
    else:
        stdout = stderr = stdlog = None

    if 'transformation' in job and job['transformation'] is not None and job['transformation'].startswith('http'):
        job['transformation'] = "<a href='%s'>%s</a>" % ( job['transformation'], job['transformation'].split('/')[-1] )

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
        }
        data.update(getContextVariables(request))
        return render_to_response('jobInfo.html', data, RequestContext(request))
    elif request.META.get('CONTENT_TYPE', 'text/plain') == 'application/json':
        return  HttpResponse('json', mimetype='text/html')
    else:
        return  HttpResponse('not understood', mimetype='text/html')

def userList(request):
    sumd = []
    jobsumd = []
    userdb = []
    if VOMODE == 'atlas':
        nhours = 90*24
        startdate = datetime.utcnow() - timedelta(hours=nhours)
        startdate = startdate.strftime(defaultDatetimeFormat)
        enddate = datetime.utcnow().strftime(defaultDatetimeFormat)
        query = { 'latestjob__range' : [startdate, enddate] }
        viewParams['selection'] = ", last %d days" % (float(nhours)/24.)
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
    else:
        ## dynamically assemble user summary info
        query = setupView(request)
        jobs = QuerySetChain(\
                        Jobsdefined4.objects.filter(**query).order_by('-modificationtime')[:JOB_LIMIT],
                        Jobsactive4.objects.filter(**query).order_by('-modificationtime')[:JOB_LIMIT],
                        Jobswaiting4.objects.filter(**query).order_by('-modificationtime')[:JOB_LIMIT],
                        Jobsarchived4.objects.filter(**query).order_by('-modificationtime')[:JOB_LIMIT],
        )
        for job in jobs:
            if job.transformation: job.transformation = job.transformation.split('/')[-1]
        sumd = userSummaryDict(jobs)
        jobsumd = jobSummaryDict(jobs, [ 'jobstatus', 'prodsourcelabel', 'specialhandling', 'vo', 'transformation', ])
    if request.META.get('CONTENT_TYPE', 'text/plain') == 'text/plain':
        data = {
            'viewParams' : viewParams,
            'xurl' : extensibleURL(request),
            'url' : request.path,
            'sumd' : sumd,
            'jobsumd' : jobsumd,
            'userdb' : userdb,
        }
        data.update(getContextVariables(request))
        return render_to_response('userList.html', data, RequestContext(request))
    elif request.META.get('CONTENT_TYPE', 'text/plain') == 'application/json':
        resp = sumd
        return  HttpResponse(json_dumps(resp), mimetype='text/html')

def userInfo(request, user):
    query = setupView(request,hours=24)
    query['produsername'] = user
    jobs = QuerySetChain(\
                    Jobsdefined4.objects.filter(**query).order_by('-modificationtime')[:JOB_LIMIT],
                    Jobsactive4.objects.filter(**query).order_by('-modificationtime')[:JOB_LIMIT],
                    Jobswaiting4.objects.filter(**query).order_by('-modificationtime')[:JOB_LIMIT],
                    Jobsarchived4.objects.filter(**query).order_by('-modificationtime')[:JOB_LIMIT],
    )
    jobs = sorted(jobs, key=lambda x:-x.pandaid)
    for job in jobs:
        if job.transformation: job.transformation = job.transformation.split('/')[-1]
    if request.META.get('CONTENT_TYPE', 'text/plain') == 'text/plain':
        sumd = userSummaryDict(jobs)
        flist =  [ 'jobstatus', 'prodsourcelabel', 'processingtype', 'specialhandling', 'transformation', 'jobsetid', 'taskid', 'jeditaskid', 'computingsite', 'cloud' ]
        if VOMODE != 'atlas': flist.append('vo')
        jobsumd = jobSummaryDict(jobs, flist)
        data = {
            'viewParams' : viewParams,
            'xurl' : extensibleURL(request),
            'user' : user,
            'sumd' : sumd,
            'jobsumd' : jobsumd,
            'jobList' : jobs,
            'query' : query,
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
        for field in Schedconfig._meta.get_all_field_names():
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
    for site in sites:
        if site['maxtime'] and (site['maxtime'] > 0) : site['maxtime'] = "%.1f" % ( float(site['maxtime'])/3600. )
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
    startdate = datetime.utcnow() - timedelta(hours=LAST_N_HOURS_MAX)
    startdate = startdate.strftime(defaultDatetimeFormat)
    enddate = datetime.utcnow().strftime(defaultDatetimeFormat)
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
        attrs.append({'name' : 'Maximum memory', 'value' : "%.1f GB" % (float(siterec.maxmemory)/1000.) })
        attrs.append({'name' : 'Maximum time', 'value' : "%.1f hours" % (float(siterec.maxtime)/3600.) })
        data = {
            'viewParams' : viewParams,
            'site' : siterec,
            'colnames' : colnames,
            'attrs' : attrs,
            'name' : site,
        }
        data.update(getContextVariables(request))
        return render_to_response('siteInfo.html', data, RequestContext(request))
    elif request.META.get('CONTENT_TYPE', 'text/plain') == 'application/json':
        resp = []
        for job in jobList:
            resp.append({ 'pandaid': job.pandaid, 'status': job.jobstatus, 'prodsourcelabel': job.prodsourcelabel, 'produserid' : job.produserid})
        return  HttpResponse(json_dumps(resp), mimetype='text/html')
