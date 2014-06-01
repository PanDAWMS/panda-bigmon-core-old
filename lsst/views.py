"""
    lsst.views
"""
import json
import logging
import pytz
import re
from datetime import datetime, timedelta

from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.template import RequestContext, loader
from django.db.models import Count
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.conf import settings

from core.common.utils import getPrefix, getContextVariables, QuerySetChain
# from ..common.settings import defaultDatetimeFormat
from core.common.settings import defaultDatetimeFormat
from core.pandajob.models import PandaJob, Jobsactive4, Jobsdefined4, Jobswaiting4, Jobsarchived4, Jobsarchived
from core.resource.models import Schedconfig
from core.common.models import Filestable4 
from core.common.models import FilestableArch
from core.common.models import Users
from core.common.models import Jobparamstable
from core.common.models import Logstable
from core.common.models import JediJobRetryHistory
from core.common.models import JediTasks
from core.common.models import JediTaskparams
from core.common.models import JediEvents
# from core.common.settings.config import ENV
# use settings.ENV instead

#from settings.local import dbaccess
# use settings.DATABASES instead

from .utils import homeCloud, statelist, setupHomeCloud, sitestatelist, \
    viewParams, VOLIST, VONAME, VOMODE, \
    standard_fields, standard_sitefields, standard_taskfields, \
    setupView, cleanJobList, cleanTaskList, \
    siteSummaryDict, userSummaryDict, \
    extensibleURL, errorInfo, \
    isEventService, \
    userList, \
    siteSummary, voSummary, wnSummary, jobStateSummary, \
    LAST_N_HOURS_MAX, JOB_LIMIT


_logger = logging.getLogger('bigpandamon')





def jobSummaryDict(request, jobs, fieldlist = None):
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


def taskSummaryDict(request, tasks, fieldlist = None):
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
        return render_to_response('lsst-mainPage.html', data, RequestContext(request))
    elif request.META.get('CONTENT_TYPE', 'text/plain') == 'application/json':
        return  HttpResponse('json', mimetype='text/html')
    else:
        return  HttpResponse('not understood', mimetype='text/html')


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
                droplist.append( { 'pandaid' : pandaid, 'newpandaid' : dropJob } )
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
        return render_to_response('jobList.html', data, RequestContext(request))
    elif request.META.get('CONTENT_TYPE', 'text/plain') == 'application/json':
        resp = []
        for job in jobs:
            resp.append({ 'pandaid': job.pandaid, 'status': job.jobstatus, 'prodsourcelabel': job.prodsourcelabel, 'produserid' : job.produserid})
        return  HttpResponse(json_dumps(resp), mimetype='text/html')


@csrf_exempt
def jobInfo(request, pandaid=None, batchid=None, p2=None, p3=None, p4=None):
    query = setupView(request, hours=365*24)
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
        jobid = "'"+batchid+"'"
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
        stderr = stdout.replace('.out','.err')
        stdlog = stdout.replace('.out','.log')
    else:
        stdout = stderr = stdlog = None

    if 'transformation' in job and job['transformation'] is not None and job['transformation'].startswith('http'):
        job['transformation'] = "<a href='%s'>%s</a>" % ( job['transformation'], job['transformation'].split('/')[-1] )

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
            lsstParams = re.match('.*PIPELINE_TASK\=([a-zA-Z0-9]+).*PIPELINE_PROCESSINSTANCE\=([0-9]+).*PIPELINE_STREAM\=([0-9\.]+)',jobparams)
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
        return render_to_response('jobInfo.html', data, RequestContext(request))
    elif request.META.get('CONTENT_TYPE', 'text/plain') == 'application/json':
        return  HttpResponse('json', mimetype='text/html')
    else:
        return  HttpResponse('not understood', mimetype='text/html')


def userInfo(request, user):
    query = setupView(request,hours=24,limit=300)
    query['produsername'] = user
    jobs = []
    values = 'produsername','cloud','computingsite','cpuconsumptiontime','jobstatus','transformation','prodsourcelabel','specialhandling','vo','modificationtime','pandaid', 'atlasrelease', 'jobsetid', 'processingtype', 'workinggroup', 'jeditaskid', 'taskid', 'currentpriority', 'creationtime', 'starttime', 'endtime', 'brokerageerrorcode', 'brokerageerrordiag', 'ddmerrorcode', 'ddmerrordiag', 'exeerrorcode', 'exeerrordiag', 'jobdispatchererrorcode', 'jobdispatchererrordiag', 'piloterrorcode', 'piloterrordiag', 'superrorcode', 'superrordiag', 'taskbuffererrorcode', 'taskbuffererrordiag', 'transexitcode'
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
            userstats[field] = "%0.1f" % ( float(userstats[field])/3600.)
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
        flist =  [ 'jobstatus', 'prodsourcelabel', 'processingtype', 'specialhandling', 'transformation', 'jobsetid', 'taskid', 'jeditaskid', 'computingsite', 'cloud', 'workinggroup', ]
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
        return render_to_response('userInfo.html', data, RequestContext(request))
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
            if (site['multicloud'] == 'None') or (not re.match('[A-Z]+',site['multicloud'])): continue
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
        if site['maxtime'] and (site['maxtime'] > 0) : site['maxtime'] = "%.1f" % ( float(site['maxtime'])/3600. )
    if request.META.get('CONTENT_TYPE', 'text/plain') == 'text/plain':
        sumd = siteSummaryDict(sites)
        data = {
            'viewParams' : viewParams,
            'sites': sites,
            'sumd' : sumd,
            'xurl' : extensibleURL(request),
        }
        #data.update(getContextVariables(request))
        return render_to_response('siteList.html', data, RequestContext(request))
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


def dashboard(request, view=''):
#    if dbaccess['default']['ENGINE'].find('oracle') >= 0:
    if settings.DATABASES['default']['ENGINE'].find('oracle') >= 0:
        VOMODE = 'atlas'
    else:
        VOMODE = ''
    if VOMODE != 'atlas':
        hours = 24*7
    else:
        hours = 12
    query = setupView(request,hours=hours,limit=999999,opmode=view)

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
                    vos[vo]['pctfail'] = "%2d" % (100.*float(vos[vo]['states']['failed']['count'])/(vos[vo]['states']['finished']['count']+vos[vo]['states']['failed']['count']))
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
        allclouds['pctfail'] = "%2d" % (100.*float(allstated['failed'])/(allstated['finished']+allstated['failed']))
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
                sites[site]['pctfail'] = "%2d" % (100.*float(sites[site]['states']['failed']['count'])/(sites[site]['states']['finished']['count']+sites[site]['states']['failed']['count']))
                if int(sites[site]['pctfail']) > 5: sites[site]['pctfail'] = "<font color=red>%s</font>" % sites[site]['pctfail']

            cloudsummary.append(sites[site])
        clouds[cloud]['summary'] = cloudsummary
        if clouds[cloud]['states']['finished']['count'] + clouds[cloud]['states']['failed']['count'] > 0:
            clouds[cloud]['pctfail'] =  "%2d" % (100.*float(clouds[cloud]['states']['failed']['count'])/(clouds[cloud]['states']['finished']['count']+clouds[cloud]['states']['failed']['count']))
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
        return render_to_response('dashboard.html', data, RequestContext(request))
    elif request.META.get('CONTENT_TYPE', 'text/plain') == 'application/json':
        resp = []
        return  HttpResponse(json_dumps(resp), mimetype='text/html')


def dashAnalysis(request):
    return dashboard(request,view='analysis')


def dashProduction(request):
    return dashboard(request,view='production')


#class QuicksearchForm(forms.Form):
#    fieldName = forms.CharField(max_length=100)


def taskList(request):
    query = setupView(request, hours=180*24, limit=9999999)
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
        sumd = taskSummaryDict(request,tasks)
        data = {
            'viewParams' : viewParams,
            'requestParams' : request.GET,
            'tasks': tasks,
            'sumd' : sumd,
            'xurl' : extensibleURL(request),
        }
        return render_to_response('taskList.html', data, RequestContext(request))
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
        return render_to_response('taskInfo.html', data, RequestContext(request))
    elif request.META.get('CONTENT_TYPE', 'text/plain') == 'application/json':
        resp = []
        return  HttpResponse(json_dumps(resp), mimetype='text/html')


def jobSummary(query):
    """ Not in use. Cannot take account of rerun jobs. """
    summary = []
    summary.extend(Jobsdefined4.objects.filter(**query).values('jobstatus')\
        .annotate(Count('jobstatus')).order_by('jobstatus'))
    summary.extend(Jobswaiting4.objects.filter(**query).values('jobstatus')\
        .annotate(Count('jobstatus')).order_by('jobstatus'))
    summary.extend(Jobsactive4.objects.filter(**query).values('jobstatus')\
        .annotate(Count('jobstatus')).order_by('jobstatus'))
    summary.extend(Jobsarchived4.objects.filter(**query).values('jobstatus')\
        .annotate(Count('jobstatus')).order_by('jobstatus'))
    summary.extend(Jobsarchived.objects.filter(**query).values('jobstatus')\
        .annotate(Count('jobstatus')).order_by('jobstatus'))
    jobstates = []
    global statelist
    for state in statelist:
        statecount = {}
        statecount['name'] = state
        statecount['count'] = 0
        for rec in summary:
            if rec['jobstatus'] == state:
                statecount['count'] = rec['jobstatus__count']
                continue
        jobstates.append(statecount)
    return jobstates


def jobSummary2(query):
    jobs = []
    jobs.extend(Jobsdefined4.objects.filter(**query).values('pandaid','jobstatus','jeditaskid'))
    jobs.extend(Jobswaiting4.objects.filter(**query).values('pandaid','jobstatus','jeditaskid'))
    jobs.extend(Jobsactive4.objects.filter(**query).values('pandaid','jobstatus','jeditaskid'))
    jobs.extend(Jobsarchived4.objects.filter(**query).values('pandaid','jobstatus','jeditaskid'))
    jobs.extend(Jobsarchived.objects.filter(**query).values('pandaid','jobstatus','jeditaskid'))
    
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
                droplist.append( { 'pandaid' : pandaid, 'newpandaid' : dropJob } )
        droplist = sorted(droplist, key=lambda x:-x['pandaid'])
        jobs = newjobs

    jobstates = []
    global statelist
    for state in statelist:
        statecount = {}
        statecount['name'] = state
        statecount['count'] = 0
        for job in jobs:
            if job['jobstatus'] == state:
                statecount['count'] += 1
                continue
        jobstates.append(statecount)
    return jobstates


