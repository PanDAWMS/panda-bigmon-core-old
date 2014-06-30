import logging, re, json, commands
from datetime import datetime, timedelta

from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.template import RequestContext, loader
from django.db.models import Count
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from core.common.utils import getPrefix, getContextVariables, QuerySetChain
from core.common.settings import STATIC_URL, FILTER_UI_ENV, defaultDatetimeFormat
from core.pandajob.models import PandaJob, Jobsactive4, Jobsdefined4, Jobswaiting4, Jobsarchived4, Jobsarchived
from core.resource.models import Schedconfig
from core.common.models import Filestable4 
from core.common.models import Datasets
from core.common.models import FilestableArch
from core.common.models import Users
from core.common.models import Jobparamstable
from core.common.models import Logstable
from core.common.models import Jobsdebug
from core.common.models import Cloudconfig
from core.common.models import Incidents
from core.common.models import Pandalog
from core.common.models import JediJobRetryHistory
from core.common.models import JediTasks
from core.common.models import JediTaskparams
from core.common.models import JediEvents
from core.common.models import JediDatasets
from core.common.models import JediDatasetContents
from core.common.models import JediWorkQueue
from core.common.settings.config import ENV

from settings.local import dbaccess

homeCloud = {}

statelist = [ 'defined', 'waiting', 'pending', 'assigned', 'throttled', 'activated', 'sent', 'starting', 'running', 'holding', 'transferring', 'finished', 'failed', 'cancelled', ]
sitestatelist = [ 'assigned', 'throttled',  'activated', 'sent', 'starting', 'running', 'holding', 'transferring', 'finished', 'failed', 'cancelled' ]
eventservicestatelist = [ 'ready', 'sent', 'running', 'finished', 'cancelled', 'discarded', 'done' ]

errorcodelist = [ 
    { 'name' : 'brokerage', 'error' : 'brokerageerrorcode', 'diag' : 'brokerageerrordiag' },
    { 'name' : 'ddm', 'error' : 'ddmerrorcode', 'diag' : 'ddmerrordiag' },
    { 'name' : 'exe', 'error' : 'exeerrorcode', 'diag' : 'exeerrordiag' },
    { 'name' : 'jobdispatcher', 'error' : 'jobdispatchererrorcode', 'diag' : 'jobdispatchererrordiag' },
    { 'name' : 'pilot', 'error' : 'piloterrorcode', 'diag' : 'piloterrordiag' },
    { 'name' : 'sup', 'error' : 'superrorcode', 'diag' : 'superrordiag' },
    { 'name' : 'taskbuffer', 'error' : 'taskbuffererrorcode', 'diag' : 'taskbuffererrordiag' },
    { 'name' : 'transformation', 'error' : 'transexitcode', 'diag' : None },
    ]


_logger = logging.getLogger('bigpandamon')
viewParams = {}

LAST_N_HOURS_MAX = 0
JOB_LIMIT = 0
TFIRST = timezone.now()
TLAST = timezone.now() - timedelta(hours=2400)
PLOW = 1000000
PHIGH = -1000000

standard_fields = [ 'processingtype', 'computingsite', 'destinationse', 'jobstatus', 'prodsourcelabel', 'produsername', 'jeditaskid', 'taskid', 'workinggroup', 'transformation', 'cloud', 'homepackage', 'inputfileproject', 'inputfiletype', 'attemptnr', 'computingelement', 'specialhandling', 'priorityrange' ]
standard_sitefields = [ 'region', 'gocname', 'nickname', 'status', 'tier', 'comment_field', 'cloud', 'allowdirectaccess', 'allowfax', 'copytool', 'faxredirector', 'retry', 'timefloor' ]
standard_taskfields = [ 'tasktype', 'status', 'corecount', 'taskpriority', 'username', 'transuses', 'transpath', 'workinggroup', 'processingtype', 'cloud', ]

VOLIST = [ 'atlas', 'bigpanda', 'htcondor', 'lsst', ]
VONAME = { 'atlas' : 'ATLAS', 'bigpanda' : 'BigPanDA', 'htcondor' : 'HTCondor', 'lsst' : 'LSST', '' : '' }
VOMODE = ' '

def setupHomeCloud():
    global homeCloud
    if len(homeCloud) > 0: return
    sites = Schedconfig.objects.filter().exclude(cloud='CMS').values()
    for site in sites:
        homeCloud[site['siteid']] = site['cloud']

def setupView(request, opmode='', hours=0, limit=-99):
    global VOMODE
    global viewParams
    global LAST_N_HOURS_MAX, JOB_LIMIT
    deepquery = False
    setupHomeCloud()
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
    fields = standard_fields
    if VOMODE == 'atlas':
        LAST_N_HOURS_MAX = 12
        if 'hours' not in request.GET:
            JOB_LIMIT = 3000
        else:
            JOB_LIMIT = 3000
        if 'cloud' not in fields: fields.append('cloud')
        if 'atlasrelease' not in fields: fields.append('atlasrelease')
        if 'produsername' in request.GET or 'jeditaskid' in request.GET:
            if 'jobsetid' not in fields: fields.append('jobsetid')
            if ('hours' not in request.GET) and ('jobsetid' in request.GET or 'taskid' in request.GET or 'jeditaskid' in request.GET):
                ## Cases where deep query is safe
                deepquery = True
        else:
            if 'jobsetid' in fields: fields.remove('jobsetid')
    else:
        fields.append('vo')
        LAST_N_HOURS_MAX = 7*24
        JOB_LIMIT = 1000
    if hours > 0:
        ## Call param overrides default hours, but not a param on the URL
        LAST_N_HOURS_MAX = hours
    ## For site-specific queries, allow longer time window
    if 'computingsite' in request.GET:
        LAST_N_HOURS_MAX = 72
    if 'jobtype' in request.GET and request.GET['jobtype'] == 'eventservice':
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
    if 'jeditaskid' in request.GET: deepquery = True
    if 'taskid' in request.GET: deepquery = True
    if 'pandaid' in request.GET: deepquery = True
    if 'jobname' in request.GET: deepquery = True
    if 'batchid' in request.GET: deepquery = True
    if deepquery:
        opmode = 'notime'
        hours = LAST_N_HOURS_MAX = 24*180
        limit = JOB_LIMIT = 999999
    if opmode != 'notime':
        if LAST_N_HOURS_MAX <= 72 :
            viewParams['selection'] = ", last %s hours" % LAST_N_HOURS_MAX
        else:
            viewParams['selection'] = ", last %d days" % (float(LAST_N_HOURS_MAX)/24.)
        if JOB_LIMIT < 100000 and JOB_LIMIT > 0:
            viewParams['selection'] += " (limit %s per table)" % JOB_LIMIT
        viewParams['selection'] += ". Query params: hours=%s" % LAST_N_HOURS_MAX
        if JOB_LIMIT < 100000 and JOB_LIMIT > 0:
            viewParams['selection'] += ", limit=%s" % JOB_LIMIT
    else:
        viewParams['selection'] = ""
    for param in request.GET:
        if request.GET[param] == 'None': continue
        if request.GET[param] == '': continue
        if param == 'display_limit': continue
        if param == 'sortby': continue
        viewParams['selection'] += ", %s=%s " % ( param, request.GET[param] )

    startdate = None
    if 'time_from' in request.GET:
        time_from = request.GET.get('time_from', 0)
        if time_from:
            time_from = float(time_from)/1000.
            startdate = datetime.utcfromtimestamp(time_from).replace(tzinfo=utc).strftime(defaultDatetimeFormat)
    if not startdate:
        startdate = datetime.utcnow() - timedelta(hours=LAST_N_HOURS_MAX)
        startdate = startdate.strftime(defaultDatetimeFormat)
    enddate = None
    if 'time_to' in request.GET:
    	time_to = request.GET.get('time_to', 0)
    	if time_to:
            time_to = float(time_to)/1000.
            enddate = datetime.utcfromtimestamp(time_to).replace(tzinfo=utc).strftime(defaultDatetimeFormat)
    if not enddate:
        enddate = datetime.utcnow().strftime(defaultDatetimeFormat)
    query = { 'modificationtime__range' : [startdate, enddate] }
    ### Add any extensions to the query determined from the URL
    for vo in [ 'atlas', 'lsst' ]:
        if request.META['HTTP_HOST'].startswith(vo):
            query['vo'] = vo   
    for param in request.GET:
        if param == 'cloud' and request.GET[param] == 'All':
            continue
        elif param == 'priorityrange':
            mat = re.match('([0-9]+)\:([0-9]+)', request.GET[param])
            if mat:
                plo = int(mat.group(1))
                phi = int(mat.group(2))
                query['currentpriority__gte'] = plo
                query['currentpriority__lte'] = phi                
        elif param == 'jobsetrange':
            mat = re.match('([0-9]+)\:([0-9]+)', request.GET[param])
            if mat:
                plo = int(mat.group(1))
                phi = int(mat.group(2))
                query['jobsetid__gte'] = plo
                query['jobsetid__lte'] = phi 
        for field in Jobsactive4._meta.get_all_field_names():
            if param == field:
                if param == 'specialhandling':
                    query['specialhandling__contains'] = request.GET[param]
                elif param == 'transformation' or param == 'transpath':
                    query['%s__endswith' % param] = request.GET[param]
                elif param == 'modificationhost' and request.GET[param].find('@') < 0:
                    query['%s__contains' % param] = request.GET[param]
                elif param == 'jeditaskid':
                    if request.GET['jeditaskid'] != 'None':
                        if int(request.GET['jeditaskid']) < 4000000:
                            query['taskid'] = request.GET[param]
                        else:
                            query[param] = request.GET[param]
                elif param == 'taskid':
                    if request.GET['taskid'] != 'None': query[param] = request.GET[param]
                elif request.GET[param].find('|') > 0:
                    vals = request.GET[param].split('|')
                    query[param+"__in"] = vals
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
    elif jobtype == 'groupproduction':
        query['prodsourcelabel'] = 'managed'
        query['workinggroup__isnull'] = False
    elif jobtype == 'eventservice':
        query['specialhandling__contains'] = 'eventservice'
    elif jobtype == 'test':
        query['prodsourcelabel__icontains'] = 'test'
    print query
    return query

def cleanJobList(jobs, mode='drop'):
    for job in jobs:
        if not job['produsername']:
            if job['produserid']:
                job['produsername'] = job['produserid']
            else:
                job['produsername'] = 'Unknown'
        if job['transformation']: job['transformation'] = job['transformation'].split('/')[-1]
        if (job['jobstatus'] == 'failed' or job['jobstatus'] == 'cancelled') and 'brokerageerrorcode' in job:
            job['errorinfo'] = errorInfo(job,nchars=70)
        else:
            job['errorinfo'] = ''
        job['jobinfo'] = ''
        if isEventService(job): job['jobinfo'] = 'Event service job'
        job['duration'] = ""
        #if job['jobstatus'] in ['finished','failed','holding']:
        if 'endtime' in job and 'starttime' in job and job['endtime'] and job['starttime']:
            job['duration'] = "%s" % (job['endtime'] - job['starttime'])
        job['waittime'] = ""
        #if job['jobstatus'] in ['running','finished','failed','holding','cancelled','transferring']:
        if 'creationtime' in job and 'starttime' in job and job['starttime'] and job['creationtime']:
            job['waittime'] = "%s" % (job['starttime'] - job['creationtime'])
        if 'currentpriority' in job:
            plo = int(job['currentpriority'])-int(job['currentpriority'])%100
            phi = plo+99
            job['priorityrange'] = "%d:%d" % ( plo, phi )
        if 'jobsetid' in job and job['jobsetid']:
            plo = int(job['jobsetid'])-int(job['jobsetid'])%100
            phi = plo+99
            job['jobsetrange'] = "%d:%d" % ( plo, phi )

    if mode == 'nodrop': return jobs
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
                    dropJob = retry['newpandaid']
            if (dropJob == 0) or isEventService(job):
                newjobs.append(job)
            else:
                droplist.append( { 'pandaid' : pandaid, 'newpandaid' : dropJob } )
        droplist = sorted(droplist, key=lambda x:-x['pandaid'])
        jobs = newjobs
    global TFIRST, TLAST, PLOW, PHIGH
    TFIRST = timezone.now()
    TLAST = timezone.now() - timedelta(hours=2400)
    PLOW = 1000000
    PHIGH = -1000000
    for job in jobs:
        if job['modificationtime'] > TLAST: TLAST = job['modificationtime']
        if job['modificationtime'] < TFIRST: TFIRST = job['modificationtime']
        if job['currentpriority'] > PHIGH: PHIGH = job['currentpriority']
        if job['currentpriority'] < PLOW: PLOW = job['currentpriority']
    jobs = sorted(jobs, key=lambda x:-x['pandaid'])
    return jobs

def cleanTaskList(tasks):
    for task in tasks:
        if task['transpath']: task['transpath'] = task['transpath'].split('/')[-1]
    return tasks

def jobSummaryDict(request, jobs, fieldlist = None):
    """ Return a dictionary summarizing the field values for the chosen most interesting fields """
    sumd = {}
    if fieldlist:
        flist = fieldlist
    else:
        flist = standard_fields
    for job in jobs:
        for f in flist:
            if f in job and job[f]:
                if f == 'taskid' and int(job[f]) < 1000000 and 'produsername' not in request.GET: continue
                if f == 'specialhandling':
                    if not 'specialhandling' in sumd: sumd['specialhandling'] = {}
                    shl = job['specialhandling'].split()
                    for v in shl:
                        if not v in sumd['specialhandling']: sumd['specialhandling'][v] = 0
                        sumd['specialhandling'][v] += 1
                else:
                    if not f in sumd: sumd[f] = {}
                    if not job[f] in sumd[f]: sumd[f][job[f]] = 0
                    sumd[f][job[f]] += 1

    ## convert to ordered lists
    suml = []
    for f in sumd:
        itemd = {}
        itemd['field'] = f
        iteml = []
        kys = sumd[f].keys()
        if f in  ( 'priorityrange', 'jobsetrange' ):
            skys = []
            for k in kys:
                skys.append( { 'key' : k, 'val' : int(k[:k.index(':')]) } )
            skys = sorted(skys, key=lambda x:x['val'])
            kys = []
            for sk in skys:
                kys.append(sk['key'])
        elif f in ( 'attemptnr', 'jeditaskid', 'taskid', ):
            kys = sorted(kys, key=lambda x:int(x))
        else:
            kys.sort()
        for ky in kys:
            iteml.append({ 'kname' : ky, 'kvalue' : sumd[f][ky] })
        if 'sortby' in request.GET and request.GET['sortby'] == 'count':
            iteml = sorted(iteml, key=lambda x:x['kvalue'], reverse=True)
        elif f not in ( 'priorityrange', 'jobsetrange', 'attemptnr', 'jeditaskid', 'taskid', ):
            iteml = sorted(iteml, key=lambda x:str(x['kname']).lower())
        itemd['list'] = iteml
        suml.append(itemd)
        suml = sorted(suml, key=lambda x:x['field'])
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
        for f in standard_sitefields:
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
        if (site['multicloud'] is not None) and (site['multicloud'] != 'None') and (re.match('[A-Z]+',site['multicloud'])):
            sumd['category']['multicloud'] += 1
        if isProd: sumd['category']['production'] += 1
    if VOMODE != 'atlas': del sumd['cloud']
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

def userSummaryDict(jobs):
    """ Return a dictionary summarizing the field values for the chosen most interesting fields """
    sumd = {}
    for job in jobs:
        if 'produsername' in job and job['produsername'] != None:
            user = job['produsername'].lower()
        else:
            user = 'Unknown'
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
            sumd[user]['latest'] = timezone.now() - timedelta(hours=2400)
            sumd[user]['pandaid'] = 0
        cloud = job['cloud']
        site = job['computingsite']
        cpu = float(job['cpuconsumptiontime'])/1.
        state = job['jobstatus']
        if job['modificationtime'] > sumd[user]['latest']: sumd[user]['latest'] = job['modificationtime']
        if job['pandaid'] > sumd[user]['pandaid']: sumd[user]['pandaid'] = job['pandaid']
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
        uitem['latest'] = sumd[u]['pandaid']
        uitem['dict'] = sumd[u]
        suml.append(uitem)
    suml = sorted(suml, key=lambda x:-x['latest'])
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

def extensibleURL(request, xurl = ''):
    """ Return a URL that is ready for p=v query extension(s) to be appended """
    if xurl == '': xurl = request.get_full_path()
    if xurl.endswith('/'): xurl = xurl[0:len(xurl)-1]
    if xurl.find('?') > 0:
        xurl += '&'
    else:
        xurl += '?'
    #if 'jobtype' in request.GET:
    #    xurl += "jobtype=%s&" % request.GET['jobtype']
    return xurl

def mainPage(request):
    setupView(request)
    if request.META.get('CONTENT_TYPE', 'text/plain') == 'text/plain':
        data = {
            'prefix': getPrefix(request),
            'viewParams' : viewParams,
            'requestParams' : request.GET,
            'npars' : len(request.GET),
        }
        data.update(getContextVariables(request))
        return render_to_response('lsst-mainPage.html', data, RequestContext(request))
    elif request.META.get('CONTENT_TYPE', 'text/plain') == 'application/json':
        return  HttpResponse('json', mimetype='text/html')
    else:
        return  HttpResponse('not understood', mimetype='text/html')

def errorInfo(job, nchars=300):
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
    if job['transexitcode'] != '' and job['transexitcode'] is not None and int(job['transexitcode']) > 0:
        errtxt += 'Transformation exit code %s' % job['transexitcode']
    if len(errtxt) > nchars:
        ret = errtxt[:nchars] + '...'
    else:
        ret = errtxt[:nchars]
    return ret

def jobList(request, mode=None, param=None):
    query = setupView(request)
    jobs = []
    values = 'produsername','cloud','computingsite','cpuconsumptiontime','jobstatus','transformation','prodsourcelabel','specialhandling','vo','modificationtime','pandaid', 'atlasrelease', 'jobsetid', 'processingtype', 'workinggroup', 'jeditaskid', 'taskid', 'currentpriority', 'creationtime', 'starttime', 'endtime', 'brokerageerrorcode', 'brokerageerrordiag', 'ddmerrorcode', 'ddmerrordiag', 'exeerrorcode', 'exeerrordiag', 'jobdispatchererrorcode', 'jobdispatchererrordiag', 'piloterrorcode', 'piloterrordiag', 'superrorcode', 'superrordiag', 'taskbuffererrorcode', 'taskbuffererrordiag', 'transexitcode', 'destinationse', 'homepackage', 'inputfileproject', 'inputfiletype', 'attemptnr', 'jobname', 'computingelement'
    jobs.extend(Jobsdefined4.objects.filter(**query)[:JOB_LIMIT].values(*values))
    jobs.extend(Jobsactive4.objects.filter(**query)[:JOB_LIMIT].values(*values))
    jobs.extend(Jobswaiting4.objects.filter(**query)[:JOB_LIMIT].values(*values))
    jobs.extend(Jobsarchived4.objects.filter(**query)[:JOB_LIMIT].values(*values))
    jobs.extend(Jobsarchived.objects.filter(**query)[:JOB_LIMIT].values(*values))

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
                    dropJob = retry['newpandaid']
            if dropJob == 0 or isEventService(job):
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

    if 'display_limit' in request.GET and int(request.GET['display_limit']) < njobs:
        display_limit = int(request.GET['display_limit'])
        url_nolimit = removeParam(request.get_full_path(), 'display_limit')
    else:
        display_limit = 3000
        url_nolimit = request.get_full_path()
    njobsmax = display_limit

    if 'sortby' in request.GET:
        sortby = request.GET['sortby']
        if sortby == 'time-ascending':
            jobs = sorted(jobs, key=lambda x:x['modificationtime'])
        if sortby == 'time-descending':
            jobs = sorted(jobs, key=lambda x:x['modificationtime'], reverse=True)
        elif sortby == 'priority':
            jobs = sorted(jobs, key=lambda x:x['currentpriority'], reverse=True)
        elif sortby == 'attemptnr':
            jobs = sorted(jobs, key=lambda x:x['attemptnr'], reverse=True)
        elif sortby == 'PandaID':
            pass
    else:
        sortby = "PandaID"

    if request.META.get('CONTENT_TYPE', 'text/plain') == 'text/plain':
        sumd = jobSummaryDict(request, jobs)
        xurl = extensibleURL(request)
        nosorturl = removeParam(xurl, 'sortby',mode='extensible')
        nosorturl = removeParam(nosorturl, 'display_limit', mode='extensible')
        data = {
            'prefix': getPrefix(request),
            'viewParams' : viewParams,
            'requestParams' : request.GET,
            'jobList': jobs[:njobsmax],
            'jobtype' : jobtype,
            'njobs' : njobs,
            'user' : None,
            'sumd' : sumd,
            'xurl' : xurl,
            'droplist' : droplist,
            'ndrops' : len(droplist),
            'tfirst' : TFIRST,
            'tlast' : TLAST,
            'plow' : PLOW,
            'phigh' : PHIGH,
            'url_nolimit' : url_nolimit,
            'display_limit' : display_limit,
            'sortby' : sortby,
            'nosorturl' : nosorturl,
        }
        data.update(getContextVariables(request))
        return render_to_response('jobList.html', data, RequestContext(request))
    elif request.META.get('CONTENT_TYPE', 'text/plain') == 'application/json':
        resp = []
        for job in jobs:
            resp.append({ 'pandaid': job.pandaid, 'status': job.jobstatus, 'prodsourcelabel': job.prodsourcelabel, 'produserid' : job.produserid})
        return  HttpResponse(json_dumps(resp), mimetype='text/html')

def isEventService(job):
    if 'specialhandling' in job and ( job['specialhandling'].find('eventservice') >= 0 or job['specialhandling'].find('esmerge') >= 0 ):
        return True
    else:
        return False

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
    startdate = datetime.utcnow() - timedelta(hours=LAST_N_HOURS_MAX)
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

    ## Check for debug info
    if 'specialhandling' in job and job['specialhandling'].find('debug') >= 0:
        debugmode = True
    else:
        debugmode = False
    debugstdout = None
    if debugmode:
        if 'showdebug' in request.GET:
            debugstdoutrec = Jobsdebug.objects.filter(pandaid=pandaid).values()
            if len(debugstdoutrec) > 0:
                debugstdout = debugstdoutrec['stdout']

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
            logfile['scope'] = file['scope']
        file['fsize'] = int(file['fsize']/1000000)

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

    dsfiles = []
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
        ## for ES jobs, prepare the event table
        evtable = JediEvents.objects.filter(pandaid=job['pandaid']).values()
        fileids = {}
        datasetids = {}
        for evrange in evtable:
            fileids[int(evrange['fileid'])] = {}
            datasetids[int(evrange['datasetid'])] = {}
        flist = []
        for f in fileids:
            flist.append(f)
        dslist = []
        for ds in datasetids:
            dslist.append(ds)
        datasets = JediDatasets.objects.filter(datasetid__in=dslist).values()
        dsfiles = JediDatasetContents.objects.filter(fileid__in=flist).values()        
        for ds in datasets:
            datasetids[int(ds['datasetid'])]['dict'] = ds
        for f in dsfiles:
            fileids[int(f['fileid'])]['dict'] = f
        for evrange in evtable:
            evrange['fileid'] = fileids[int(evrange['fileid'])]['dict']['lfn']
            evrange['datasetid'] = datasetids[evrange['datasetid']]['dict']['datasetname']
            evrange['status'] = eventservicestatelist[evrange['status']]
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
            'requestParams' : request.GET,
            'pandaid': pandaid,
            'job': job,
            'columns' : columns,
            'files' : files,
            'dsfiles' : dsfiles,
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
            'debugmode' : debugmode,
            'debugstdout' : debugstdout,
        }
        data.update(getContextVariables(request))
        return render_to_response('jobInfo.html', data, RequestContext(request))
    elif request.META.get('CONTENT_TYPE', 'text/plain') == 'application/json':
        return  HttpResponse('json', mimetype='text/html')
    else:
        return  HttpResponse('not understood', mimetype='text/html')

def userList(request):
    nhours = 90*24
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
        startdate = datetime.utcnow() - timedelta(hours=nhours)
        startdate = startdate.strftime(defaultDatetimeFormat)
        enddate = datetime.utcnow().strftime(defaultDatetimeFormat)
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
            if u.cpua1: udict['cpua1'] = "%0.1f" % (int(u.cpua1)/3600.)
            if u.cpua7: udict['cpua7'] = "%0.1f" % (int(u.cpua7)/3600.)
            if u.cpup1: udict['cpup1'] = "%0.1f" % (int(u.cpup1)/3600.)
            if u.cpup7: udict['cpup7'] = "%0.1f" % (int(u.cpup7)/3600.)
            udict['latestjob'] = u.latestjob
            userdbl.append(udict)

            if u.njobsa > 0: anajobs += u.njobsa
            if u.njobsa >= 1000: n1000 += 1
            if u.njobsa >= 10000: n10k += 1
            if u.latestjob != None:
                latest = datetime.utcnow() - u.latestjob.replace(tzinfo=None)
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
            nhours = 7*24
        query = setupView(request, hours=nhours, limit=3000)
        ## dynamically assemble user summary info
        values = 'produsername','cloud','computingsite','cpuconsumptiontime','jobstatus','transformation','prodsourcelabel','specialhandling','vo','modificationtime','pandaid', 'atlasrelease', 'processingtype', 'workinggroup', 'currentpriority'
        jobs = QuerySetChain(\
                        Jobsdefined4.objects.filter(**query).order_by('-modificationtime')[:JOB_LIMIT].values(*values),
                        Jobsactive4.objects.filter(**query).order_by('-modificationtime')[:JOB_LIMIT].values(*values),
                        Jobswaiting4.objects.filter(**query).order_by('-modificationtime')[:JOB_LIMIT].values(*values),
                        Jobsarchived4.objects.filter(**query).order_by('-modificationtime')[:JOB_LIMIT].values(*values),
        )
        jobs = cleanJobList(jobs)
        sumd = userSummaryDict(jobs)
        sumparams = [ 'jobstatus', 'prodsourcelabel', 'specialhandling', 'transformation', 'processingtype', 'workinggroup', 'priorityrange', 'jobsetrange' ]
        if VOMODE == 'atlas':
            sumparams.append('atlasrelease')
        else:
            sumparams.append('vo')
        jobsumd = jobSummaryDict(request, jobs, sumparams)
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
            'tfirst' : TFIRST,
            'tlast' : TLAST,
            'plow' : PLOW,
            'phigh' : PHIGH,
        }
        data.update(getContextVariables(request))
        return render_to_response('userList.html', data, RequestContext(request))
    elif request.META.get('CONTENT_TYPE', 'text/plain') == 'application/json':
        resp = sumd
        return  HttpResponse(json_dumps(resp), mimetype='text/html')

def userInfo(request, user=''):
    if user == '':
        if 'user' in request.GET: user = request.GET['user']
        if 'produsername' in request.GET: user = request.GET['produsername']

    ## Tasks owned by the user
    startdate = datetime.utcnow() - timedelta(hours=90*24)
    startdate = startdate.strftime(defaultDatetimeFormat)
    enddate = datetime.utcnow().strftime(defaultDatetimeFormat)
    query = { 'modificationtime__range' : [startdate, enddate] }
    query['username'] = user
    tasks = JediTasks.objects.filter(**query).values()
    tasks = cleanTaskList(tasks)
    tasks = sorted(tasks, key=lambda x:-x['jeditaskid'])
    ntasks = len(tasks)

    limit = 2000
    query = setupView(request,hours=72,limit=limit)
    query['produsername__iexact'] = user
    jobs = []
    values = 'produsername','cloud','computingsite','cpuconsumptiontime','jobstatus','transformation','prodsourcelabel','specialhandling','vo','modificationtime','pandaid', 'atlasrelease', 'jobsetid', 'processingtype', 'workinggroup', 'jeditaskid', 'taskid', 'currentpriority', 'creationtime', 'starttime', 'endtime', 'brokerageerrorcode', 'brokerageerrordiag', 'ddmerrorcode', 'ddmerrordiag', 'exeerrorcode', 'exeerrordiag', 'jobdispatchererrorcode', 'jobdispatchererrordiag', 'piloterrorcode', 'piloterrordiag', 'superrorcode', 'superrordiag', 'taskbuffererrorcode', 'taskbuffererrordiag', 'transexitcode', 'homepackage', 'inputfileproject', 'inputfiletype', 'attemptnr', 'jobname'
    jobs.extend(Jobsdefined4.objects.filter(**query)[:JOB_LIMIT].values(*values))
    jobs.extend(Jobsactive4.objects.filter(**query)[:JOB_LIMIT].values(*values))
    jobs.extend(Jobswaiting4.objects.filter(**query)[:JOB_LIMIT].values(*values))
    jobs.extend(Jobsarchived4.objects.filter(**query)[:JOB_LIMIT].values(*values))
    jobsetids = None
    if len(jobs) == 0 or (len(jobs) < limit and LAST_N_HOURS_MAX > 72):
        jobs.extend(Jobsarchived.objects.filter(**query)[:JOB_LIMIT].values(*values))
#         if len(jobs) < limit and ntasks == 0:
#             ## try at least to find some old jobsets
#             startdate = datetime.utcnow() - timedelta(hours=30*24)
#             startdate = startdate.strftime(defaultDatetimeFormat)
#             enddate = datetime.utcnow().strftime(defaultDatetimeFormat)
#             query = { 'modificationtime__range' : [startdate, enddate] }
#             query['produsername'] = user
#             jobsetids = Jobsarchived.objects.filter(**query).values('jobsetid').distinct()
    jobs = cleanJobList(jobs)
    query = { 'name__iexact' : user }
    userdb = Users.objects.filter(**query).values()
    if len(userdb) > 0:
        userstats = userdb[0]
        user = userstats['name']
        for field in ['cpua1', 'cpua7', 'cpup1', 'cpup7' ]:
            try:
                userstats[field] = "%0.1f" % ( float(userstats[field])/3600.)
            except:
                userstats[field] = '-'
    else:
        userstats = None

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
        tfirst = timezone.now()
        tlast = timezone.now() - timedelta(hours=2400)
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

    njobsmax = len(jobs)
    if 'display_limit' in request.GET and int(request.GET['display_limit']) < len(jobs):
        display_limit = int(request.GET['display_limit'])
        njobsmax = display_limit
        url_nolimit = removeParam(request.get_full_path(), 'display_limit')
    else:
        display_limit = 3000
        njobsmax = display_limit
        url_nolimit = request.get_full_path()

    if request.META.get('CONTENT_TYPE', 'text/plain') == 'text/plain':
        sumd = userSummaryDict(jobs)
        flist =  [ 'jobstatus', 'prodsourcelabel', 'processingtype', 'specialhandling', 'transformation', 'jobsetid', 'taskid', 'jeditaskid', 'computingsite', 'cloud', 'workinggroup', 'homepackage', 'inputfileproject', 'inputfiletype', 'attemptnr', 'priorityrange', 'jobsetrange' ]
        if VOMODE != 'atlas':
            flist.append('vo')
        else:
            flist.append('atlasrelease')
        jobsumd = jobSummaryDict(request, jobs, flist)
        njobsetmax = 100
        data = {
            'viewParams' : viewParams,
            'requestParams' : request.GET,
            'xurl' : extensibleURL(request),
            'user' : user,
            'sumd' : sumd,
            'jobsumd' : jobsumd,
            'jobList' : jobs[:njobsmax],
            'njobs' : len(jobs),
            'query' : query,
            'userstats' : userstats,
            'tfirst' : TFIRST,
            'tlast' : TLAST,
            'plow' : PLOW,
            'phigh' : PHIGH,
            'jobsets' : jobsetl[:njobsetmax-1],
            'njobsetmax' : njobsetmax,
            'njobsets' : len(jobsetl),
            'url_nolimit' : url_nolimit,
            'display_limit' : display_limit,
            'tasks': tasks,
            'ntasks' : ntasks,
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
    mcpres = Schedconfig.objects.filter(status='online').exclude(cloud='CMS').exclude(siteid__icontains='test').values('siteid','multicloud','cloud').order_by('siteid')
    sites = []
    for site in siteres:
        if 'category' in request.GET and request.GET['category'] == 'multicloud':
            if (site['multicloud'] == 'None') or (not re.match('[A-Z]+',site['multicloud'])): continue
        sites.append(site)
    if 'sortby' in request.GET and request.GET['sortby'] == 'maxmemory':
        sites = sorted(sites, key=lambda x:-x['maxmemory'])
    elif 'sortby' in request.GET and request.GET['sortby'] == 'maxtime':
        sites = sorted(sites, key=lambda x:-x['maxtime'])
    elif 'sortby' in request.GET and request.GET['sortby'] == 'gocname':
        sites = sorted(sites, key=lambda x:x['gocname'])
    else:
        sites = sorted(sites, key=lambda x:x['siteid'])
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
        site['space'] = "%d" % (site['space']/1000.)

    if VOMODE == 'atlas' and (len(request.GET) == 0 or 'cloud' in request.GET):
        clouds = Cloudconfig.objects.filter().exclude(name='CMS').exclude(name='OSG').values()
        clouds = sorted(clouds, key=lambda x:x['name'])
        mcpsites = {}
        for cloud in clouds:
            cloud['display'] = True
            if 'cloud' in request.GET and request.GET['cloud'] != cloud['name']: cloud['display'] = False
            mcpsites[cloud['name']] = []
            for site in sites:
                if site['siteid'] == cloud['tier1']:
                    cloud['space'] = site['space']
                    cloud['tspace'] = site['tspace']
            for site in mcpres:
                mcpclouds = site['multicloud'].split(',')
                if cloud['name'] in mcpclouds or cloud['name'] == site['cloud']:
                    sited = {}
                    sited['name'] = site['siteid']
                    sited['cloud'] = site['cloud']
                    if site['cloud'] == cloud['name']:
                        sited['type'] = 'home'
                    else:
                        sited['type'] = 'mcp'
                    mcpsites[cloud['name']].append(sited)
            cloud['mcpsites'] = ''
            for s in mcpsites[cloud['name']]:
                if s['type'] == 'home':
                    cloud['mcpsites'] += "<b>%s</b> &nbsp; " % s['name']
                else:
                    cloud['mcpsites'] += "%s &nbsp; " % s['name']
    else:
        clouds = None
    xurl = extensibleURL(request)
    nosorturl = removeParam(xurl, 'sortby',mode='extensible')
    if request.META.get('CONTENT_TYPE', 'text/plain') == 'text/plain':
        sumd = siteSummaryDict(sites)
        data = {
            'viewParams' : viewParams,
            'requestParams' : request.GET,
            'sites': sites,
            'clouds' : clouds,
            'sumd' : sumd,
            'xurl' : xurl,
            'nosorturl' : nosorturl,
        }
        if 'cloud' in request.GET: data['mcpsites'] = mcpsites[request.GET['cloud']]
        #data.update(getContextVariables(request))
        return render_to_response('siteList.html', data, RequestContext(request))
    elif request.META.get('CONTENT_TYPE', 'text/plain') == 'application/json':
        resp = sites
        return  HttpResponse(json_dumps(resp), mimetype='text/html')

def siteInfo(request, site=''):
    if site == '' and 'site' in request.GET: site = request.GET['site']
    setupView(request)
    startdate = datetime.utcnow() - timedelta(hours=LAST_N_HOURS_MAX)
    startdate = startdate.strftime(defaultDatetimeFormat)
    enddate = datetime.utcnow().strftime(defaultDatetimeFormat)
    query = {'siteid__iexact' : site}
    sites = Schedconfig.objects.filter(**query)
    colnames = []
    try:
        siterec = sites[0]
        colnames = siterec.get_all_fields()
    except IndexError:
        siterec = None

    if request.META.get('CONTENT_TYPE', 'text/plain') == 'text/plain':
        attrs = []
        if siterec:
            attrs.append({'name' : 'GOC name', 'value' : siterec.gocname })
            attrs.append({'name' : 'Queue (nickname)', 'value' : siterec.nickname })
            attrs.append({'name' : 'Total queues for this site', 'value' : len(sites) })
            attrs.append({'name' : 'Status', 'value' : siterec.status })
            attrs.append({'name' : 'Comment', 'value' : siterec.comment_field })
            attrs.append({'name' : 'Last modified', 'value' : "%s" % (siterec.lastmod.strftime('%Y-%m-%d %H:%M')) })
            attrs.append({'name' : 'Cloud', 'value' : siterec.cloud })
            attrs.append({'name' : 'Multicloud', 'value' : siterec.multicloud })
            attrs.append({'name' : 'Tier', 'value' : siterec.tier })
            attrs.append({'name' : 'DDM endpoint', 'value' : siterec.ddm })
            attrs.append({'name' : 'Maximum memory', 'value' : "%.1f GB" % (float(siterec.maxmemory)/1000.) })
            attrs.append({'name' : 'Maximum time', 'value' : "%.1f hours" % (float(siterec.maxtime)/3600.) })
            attrs.append({'name' : 'Space', 'value' : "%d TB as of %s" % ((float(siterec.space)/1000.), siterec.tspace.strftime('%m-%d %H:%M')) })

            iquery = {}
            startdate = datetime.utcnow() - timedelta(hours=24*30)
            startdate = startdate.strftime(defaultDatetimeFormat)
            enddate = datetime.utcnow().strftime(defaultDatetimeFormat)
            iquery['at_time__range'] = [startdate, enddate]
            iquery['description__contains'] = 'queue=%s' % siterec.nickname
            incidents = Incidents.objects.filter(**iquery).order_by('at_time').reverse().values()
        else:
            incidents = []
        data = {
            'viewParams' : viewParams,
            'site' : siterec,
            'queues' : sites,
            'colnames' : colnames,
            'attrs' : attrs,
            'incidents' : incidents,
            'name' : site,
        }
        data.update(getContextVariables(request))
        return render_to_response('siteInfo.html', data, RequestContext(request))
    elif request.META.get('CONTENT_TYPE', 'text/plain') == 'application/json':
        resp = []
        for job in jobList:
            resp.append({ 'pandaid': job.pandaid, 'status': job.jobstatus, 'prodsourcelabel': job.prodsourcelabel, 'produserid' : job.produserid})
        return  HttpResponse(json_dumps(resp), mimetype='text/html')

def siteSummary(query):
    summary = []
    summary.extend(Jobsactive4.objects.filter(**query).values('cloud','computingsite','jobstatus').annotate(Count('jobstatus')).order_by('cloud','computingsite','jobstatus'))
    summary.extend(Jobsdefined4.objects.filter(**query).values('cloud','computingsite','jobstatus').annotate(Count('jobstatus')).order_by('cloud','computingsite','jobstatus'))
    summary.extend(Jobswaiting4.objects.filter(**query).values('cloud','computingsite','jobstatus').annotate(Count('jobstatus')).order_by('cloud','computingsite','jobstatus'))
    summary.extend(Jobsarchived4.objects.filter(**query).values('cloud','computingsite','jobstatus').annotate(Count('jobstatus')).order_by('cloud','computingsite','jobstatus'))
    return summary

def voSummary(query):
    summary = []
    summary.extend(Jobsactive4.objects.filter(**query).values('vo','jobstatus').annotate(Count('jobstatus')))
    summary.extend(Jobsdefined4.objects.filter(**query).values('vo','jobstatus').annotate(Count('jobstatus')))
    summary.extend(Jobswaiting4.objects.filter(**query).values('vo','jobstatus').annotate(Count('jobstatus')))
    summary.extend(Jobsarchived4.objects.filter(**query).values('vo','jobstatus').annotate(Count('jobstatus')))
    return summary

def wgSummary(query):
    summary = []
    summary.extend(Jobsdefined4.objects.filter(**query).values('workinggroup','jobstatus').annotate(Count('jobstatus')))
    summary.extend(Jobsactive4.objects.filter(**query).values('workinggroup','jobstatus').annotate(Count('jobstatus')))
    summary.extend(Jobswaiting4.objects.filter(**query).values('workinggroup','jobstatus').annotate(Count('jobstatus')))
    summary.extend(Jobsarchived4.objects.filter(**query).values('workinggroup','jobstatus').annotate(Count('jobstatus')))
    return summary

def wnSummary(query):
    summary = []
    summary.extend(Jobsactive4.objects.filter(**query).values('modificationhost', 'jobstatus').annotate(Count('jobstatus')).order_by('modificationhost', 'jobstatus'))
    summary.extend(Jobsarchived4.objects.filter(**query).values('modificationhost', 'jobstatus').annotate(Count('jobstatus')).order_by('modificationhost', 'jobstatus'))
    return summary

def wnInfo(request,site,wnname='all'):
    """ Give worker node level breakdown of site activity. Spot hot nodes, error prone nodes. """
    errthreshold = 15
    if wnname != 'all':
        query = setupView(request,hours=72,limit=999999)
        query['modificationhost__endswith'] = wnname
    else:
        query = setupView(request,hours=72,limit=999999)
    query['computingsite'] = site
    wnsummarydata = wnSummary(query)
    totstates = {}
    totjobs = 0
    wns = {}
    wnPlotFailed = {}
    wnPlotFinished = {}
    for state in sitestatelist:
        totstates[state] = 0
    for rec in wnsummarydata:
        jobstatus = rec['jobstatus']
        count = rec['jobstatus__count']
        wnfull = rec['modificationhost']
        wnsplit = wnfull.split('@')
        if len(wnsplit) == 2:
            if wnname == 'all': 
                wn = wnsplit[1]
            else:
                wn = wnfull
            slot = wnsplit[0]
        else:
            wn = wnfull
            slot = '1'
        if wn.startswith('aipanda'): continue
        if jobstatus == 'failed':
            if not wn in wnPlotFailed: wnPlotFailed[wn] = 0
            wnPlotFailed[wn] += count
        elif jobstatus == 'finished':
            if not wn in wnPlotFinished: wnPlotFinished[wn] = 0
            wnPlotFinished[wn] += count
        totjobs += count
        totstates[jobstatus] += count
        if wn not in wns:
            wns[wn] = {}
            wns[wn]['name'] = wn
            wns[wn]['count'] = 0
            wns[wn]['states'] = {}
            wns[wn]['slotd'] = {}
            wns[wn]['statelist'] = []
            for state in sitestatelist:
                wns[wn]['states'][state] = {}
                wns[wn]['states'][state]['name'] = state
                wns[wn]['states'][state]['count'] = 0
        if slot not in wns[wn]['slotd']: wns[wn]['slotd'][slot] = 0
        wns[wn]['slotd'][slot] += 1
        wns[wn]['count'] += count
        wns[wn]['states'][jobstatus]['count'] += count

    ## Convert dict to summary list
    wnkeys = wns.keys()
    wnkeys.sort()
    wntot = len(wnkeys)
    fullsummary = []

    allstated = {}
    allstated['finished'] = allstated['failed'] = 0
    allwns = {}
    allwns['name'] = 'All'
    allwns['count'] = totjobs
    allwns['states'] = totstates
    allwns['statelist'] = []
    for state in sitestatelist:
        allstate = {}
        allstate['name'] = state
        allstate['count'] = totstates[state]
        allstated[state] = totstates[state]
        allwns['statelist'].append(allstate)
    if int(allstated['finished']) + int(allstated['failed']) > 0:
        allwns['pctfail'] = int(100.*float(allstated['failed'])/(allstated['finished']+allstated['failed']))
    else:
        allwns['pctfail'] = 0
    if wnname == 'all': fullsummary.append(allwns)
    avgwns = {}
    avgwns['name'] = 'Average'
    if wntot > 0:
        avgwns['count'] = "%0.2f" % (totjobs/wntot)
    else:
        avgwns['count'] = ''
    avgwns['states'] = totstates
    avgwns['statelist'] = []
    avgstates = {}
    for state in sitestatelist:
        if wntot > 0:
            avgstates[state] = totstates[state]/wntot
        else:
            avgstates[state] = ''
        allstate = {}
        allstate['name'] = state
        if wntot > 0:
            allstate['count'] = "%0.2f" % (int(totstates[state])/wntot)
            allstated[state] = "%0.2f" % (int(totstates[state])/wntot)
        else:
            allstate['count'] = ''
            allstated[state] = ''
        avgwns['statelist'].append(allstate)
        avgwns['pctfail'] = allwns['pctfail']
    if wnname == 'all': fullsummary.append(avgwns)

    for wn in wnkeys:
        outlier = ''
        wns[wn]['slotcount'] = len(wns[wn]['slotd'])
        wns[wn]['pctfail'] = 0
        for state in sitestatelist:
            wns[wn]['statelist'].append(wns[wn]['states'][state])      
        if wns[wn]['states']['finished']['count'] + wns[wn]['states']['failed']['count'] > 0:
            wns[wn]['pctfail'] = int(100.*float(wns[wn]['states']['failed']['count'])/(wns[wn]['states']['finished']['count']+wns[wn]['states']['failed']['count']))
        if float(wns[wn]['states']['finished']['count']) < float(avgstates['finished'])/5. :
            outlier += " LowFinished "
        if float(wns[wn]['states']['failed']['count']) > float(avgstates['failed'])*3. :
            outlier += " HighFailed "
        wns[wn]['outlier'] = outlier
        fullsummary.append(wns[wn])

    if 'sortby' in request.GET:
        if request.GET['sortby'] in sitestatelist:
            fullsummary = sorted(fullsummary, key=lambda x:x['states'][request.GET['sortby']],reverse=True)
        elif request.GET['sortby'] == 'pctfail':
            fullsummary = sorted(fullsummary, key=lambda x:x['pctfail'],reverse=True)

    kys = wnPlotFailed.keys()
    kys.sort()
    wnPlotFailedL = []
    for k in kys:
        wnPlotFailedL.append( [ k, wnPlotFailed[k] ] )

    kys = wnPlotFinished.keys()
    kys.sort()
    wnPlotFinishedL = []
    for k in kys:
        wnPlotFinishedL.append( [ k, wnPlotFinished[k] ] )

    if request.META.get('CONTENT_TYPE', 'text/plain') == 'text/plain':
        xurl = extensibleURL(request)
        data = {
            'viewParams' : viewParams,
            'requestParams' : request.GET,
            'url' : request.path,
            'xurl' : xurl,
            'site' : site,
            'wnname' : wnname,
            'user' : None,
            'summary' : fullsummary,
            'wnPlotFailed' : wnPlotFailedL,
            'wnPlotFinished' : wnPlotFinishedL,
            'hours' : LAST_N_HOURS_MAX,
            'errthreshold' : errthreshold,
        }
        return render_to_response('wnInfo.html', data, RequestContext(request))
    elif request.META.get('CONTENT_TYPE', 'text/plain') == 'application/json':
        resp = []
        return  HttpResponse(json_dumps(resp), mimetype='text/html')

def dashboard(request, view=''):
    errthreshold = 10
    if dbaccess['default']['ENGINE'].find('oracle') >= 0:
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
                    vos[vo]['pctfail'] = int(100.*float(vos[vo]['states']['failed']['count'])/(vos[vo]['states']['finished']['count']+vos[vo]['states']['failed']['count']))
            vosummary.append(vos[vo])

        if 'sortby' in request.GET:
            if request.GET['sortby'] in statelist:
                vosummary = sorted(vosummary, key=lambda x:x['states'][request.GET['sortby']],reverse=True)
            elif request.GET['sortby'] == 'pctfail':
                vosummary = sorted(vosummary, key=lambda x:x['pctfail'],reverse=True)

    else:
        if view == 'production':
            errthreshold = 5
        else:
            errthreshold = 15
        vosummary = []

    if VOMODE == 'atlas' and len(request.GET) == 0:
        cloudinfol = Cloudconfig.objects.filter().exclude(name='CMS').exclude(name='OSG').values('name','status')
    else:
        cloudinfol = []
    cloudinfo = {}
    for c in cloudinfol:
        cloudinfo[c['name']] = c['status']

    siteinfol = Schedconfig.objects.filter().exclude(cloud='CMS').values('siteid','status')
    siteinfo = {}
    for s in siteinfol:
        siteinfo[s['siteid']] = s['status']    

    cloudview = 'cloud'
    if 'cloudview' in request.GET:
        cloudview = request.GET['cloudview']
    if view != 'production': cloudview = 'N/A'
    sitesummarydata = siteSummary(query)
    clouds = {}
    totstates = {}
    totjobs = 0
    for state in sitestatelist:
        totstates[state] = 0
    for rec in sitesummarydata:
        if cloudview == 'region':
            if rec['computingsite'] in homeCloud:
                cloud = homeCloud[rec['computingsite']]
            else:
                print "ERROR cloud not known", rec
                cloud = ''
        else:
            cloud = rec['cloud']
        site = rec['computingsite']
        jobstatus = rec['jobstatus']
        count = rec['jobstatus__count']
        if jobstatus not in sitestatelist: continue
        totjobs += count
        totstates[jobstatus] += count
        if cloud not in clouds:
            clouds[cloud] = {}
            clouds[cloud]['name'] = cloud
            if cloud in cloudinfo: clouds[cloud]['status'] = cloudinfo[cloud]
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
            if site in siteinfo: clouds[cloud]['sites'][site]['status'] = siteinfo[site]
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
        allclouds['pctfail'] = int(100.*float(allstated['failed'])/(allstated['finished']+allstated['failed']))
    else:
        allclouds['pctfail'] = 0
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
                sites[site]['pctfail'] = int(100.*float(sites[site]['states']['failed']['count'])/(sites[site]['states']['finished']['count']+sites[site]['states']['failed']['count']))
            else:
                sites[site]['pctfail'] = 0

            cloudsummary.append(sites[site])
        clouds[cloud]['summary'] = cloudsummary
        if clouds[cloud]['states']['finished']['count'] + clouds[cloud]['states']['failed']['count'] > 0:
            clouds[cloud]['pctfail'] =  int(100.*float(clouds[cloud]['states']['failed']['count'])/(clouds[cloud]['states']['finished']['count']+clouds[cloud]['states']['failed']['count']))

        fullsummary.append(clouds[cloud])

    if 'sortby' in request.GET:
        if request.GET['sortby'] in statelist:
            fullsummary = sorted(fullsummary, key=lambda x:x['states'][request.GET['sortby']],reverse=True)
            cloudsummary = sorted(cloudsummary, key=lambda x:x['states'][request.GET['sortby']],reverse=True)
            for cloud in clouds:
                clouds[cloud]['summary'] = sorted(clouds[cloud]['summary'], key=lambda x:x['states'][request.GET['sortby']]['count'],reverse=True)
        elif request.GET['sortby'] == 'pctfail':
            fullsummary = sorted(fullsummary, key=lambda x:x['pctfail'],reverse=True)
            cloudsummary = sorted(cloudsummary, key=lambda x:x['pctfail'],reverse=True)
            for cloud in clouds:
                clouds[cloud]['summary'] = sorted(clouds[cloud]['summary'], key=lambda x:x['pctfail'],reverse=True)

    if request.META.get('CONTENT_TYPE', 'text/plain') == 'text/plain':
        xurl = extensibleURL(request)
        nosorturl = removeParam(xurl, 'sortby',mode='extensible')
        data = {
            'viewParams' : viewParams,
            'requestParams' : request.GET,
            'url' : request.path,
            'xurl' : xurl,
            'nosorturl' : nosorturl,
            'user' : None,
            'summary' : fullsummary,
            'vosummary' : vosummary,
            'view' : view,
            'cloudview': cloudview,
            'hours' : hours,
            'errthreshold' : errthreshold,
        }
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
        for field in JediTasks._meta.get_all_field_names():
            if param == field:
                if param == 'transpath':
                    query['%s__endswith' % param] = request.GET[param]
                else:
                    query[param] = request.GET[param]
        if param == 'eventservice':
            query['eventservice'] = 1
    tasks = JediTasks.objects.filter(**query).values()
    tasks = cleanTaskList(tasks)
    tasks = sorted(tasks, key=lambda x:-x['jeditaskid'])
    ntasks = len(tasks)

    nmax = ntasks
    if 'display_limit' in request.GET and int(request.GET['display_limit']) < nmax:
        display_limit = int(request.GET['display_limit'])
        nmax = display_limit
        url_nolimit = removeParam(request.get_full_path(), 'display_limit')
    else:
        display_limit = 3000
        nmax = display_limit
        url_nolimit = request.get_full_path()
        
    if request.META.get('CONTENT_TYPE', 'text/plain') == 'text/plain':
        sumd = taskSummaryDict(request,tasks)
        data = {
            'viewParams' : viewParams,
            'requestParams' : request.GET,
            'tasks': tasks[:nmax],
            'ntasks' : ntasks,
            'sumd' : sumd,
            'xurl' : extensibleURL(request),
            'url_nolimit' : url_nolimit,
            'display_limit' : display_limit,
        }
        return render_to_response('taskList.html', data, RequestContext(request))
    elif request.META.get('CONTENT_TYPE', 'text/plain') == 'application/json':
        resp = sites
        return  HttpResponse(json_dumps(resp), mimetype='text/html')

def taskInfo(request, jeditaskid=0):
    setupView(request, hours=365*24, limit=999999999)
    query = {}
    tasks = []
    taskrec = None
    colnames = []
    columns = []
    jobsummary = []
    if 'jeditaskid' in request.GET: jeditaskid = request.GET['jeditaskid']
    if jeditaskid != 0:
        query = {'jeditaskid' : jeditaskid}
        jobsummary = jobSummary2(query)
        tasks = JediTasks.objects.filter(**query).values()
    elif 'taskname' in request.GET:
        querybyname = {'taskname' : request.GET['taskname'] }
        tasks = JediTasks.objects.filter(**querybyname).values()
        if len(tasks) > 0:
            jeditaskid = tasks[0]['jeditaskid']
        query = {'jeditaskid' : jeditaskid}
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
    if not taskrec['ticketid'] and taskparams:
        if 'ticketID' in taskparams: taskrec['ticketid'] = taskparams['ticketID']
        if 'ticketSystemType' in taskparams: taskrec['ticketsystemtype'] = taskparams['ticketSystemType']

    if taskrec:
        taskname = taskrec['taskname']
    elif 'taskname' in request.GET:
        taskname = request.GET['taskname']
    else:
        taskname = ''        

    logtxt = None
    if taskrec['errordialog']:
        mat = re.match('^.*"([^"]+)"',taskrec['errordialog'])
        if mat:
            errurl = mat.group(1)
            cmd = "curl -s -f --compressed '%s'" % errurl
            logpfx = u"logtxt: %s\n" % cmd
            logout = commands.getoutput(cmd)
            if len(logout) > 0: logtxt = logout

    if request.META.get('CONTENT_TYPE', 'text/plain') == 'text/plain':
        attrs = []
        if taskrec:
            attrs.append({'name' : 'Status', 'value' : taskrec['status'] })
        data = {
            'viewParams' : viewParams,
            'requestParams' : request.GET,
            'task' : taskrec,
            'taskname' : taskname,
            'taskparams' : taskparams,
            'taskparaml' : taskparaml,
            'columns' : columns,
            'attrs' : attrs,
            'jobsummary' : jobsummary,
            'jeditaskid' : jeditaskid,
            'logtxt' : logtxt,
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

def jobStateSummary(jobs):
    global statelist
    statecount = {}
    for state in statelist:
        statecount[state] = 0
    for job in jobs:
        statecount[job['jobstatus']] += 1
    return statecount

def errorSummaryDict(request,jobs):
    """ take a job list and produce error summaries from it """
    errsByCount = {}
    errsBySite = {}
    errsByUser = {}
    errsByTask = {}
    sumd = {}
    ## histogram of errors vs. time, for plotting
    errHist = {}
    flist = [ 'cloud', 'computingsite', 'produsername', 'taskid', 'jeditaskid', 'processingtype', 'prodsourcelabel', 'transformation', 'workinggroup', 'specialhandling', 'computingelement' ]

    for job in jobs:
        if job['jobstatus'] not in [ 'failed', 'transferring', 'holding' ]: continue
        site = job['computingsite']
        if 'cloud' in request.GET:
            if site in homeCloud and homeCloud[site] != request.GET['cloud']: continue
        user = job['produsername']
        if job['jeditaskid'] > 0:
            taskid = job['jeditaskid']
            tasktype = 'jeditaskid'
        else:
            taskid = job['taskid']
            tasktype = 'taskid'
        tm = job['modificationtime']
        tm = tm - timedelta(minutes=tm.minute % 30, seconds=tm.second, microseconds=tm.microsecond)
        if not tm in errHist: errHist[tm] = 0
        errHist[tm] += 1

        ## Overall summary
        for f in flist:
            if job[f]:
                if f == 'taskid' and job[f] < 1000000 and 'produsername' not in request.GET:
                    pass
                else:
                    if not f in sumd: sumd[f] = {}
                    if not job[f] in sumd[f]: sumd[f][job[f]] = 0
                    sumd[f][job[f]] += 1
        if job['specialhandling']:
            if not 'specialhandling' in sumd: sumd['specialhandling'] = {}
            shl = job['specialhandling'].split()
            for v in shl:
                if not v in sumd['specialhandling']: sumd['specialhandling'][v] = 0
                sumd['specialhandling'][v] += 1

        for err in errorcodelist:
            if job[err['error']] != 0 and  job[err['error']] != '' and job[err['error']] != None:
                errcode = "%s:%s" % ( err['name'], job[err['error']] )
                if err['diag']:
                    errdiag = job[err['diag']]
                else:
                    errdiag = ''
                    
                if errcode not in errsByCount:
                    errsByCount[errcode] = {}
                    errsByCount[errcode]['error'] = errcode
                    errsByCount[errcode]['codename'] = err['error']
                    errsByCount[errcode]['codeval'] = job[err['error']]
                    errsByCount[errcode]['diag'] = errdiag
                    errsByCount[errcode]['count'] = 0
                errsByCount[errcode]['count'] += 1
                
                if user not in errsByUser:
                    errsByUser[user] = {}
                    errsByUser[user]['name'] = user
                    errsByUser[user]['errors'] = {}
                    errsByUser[user]['toterrors'] = 0
                if errcode not in errsByUser[user]['errors']:
                    errsByUser[user]['errors'][errcode] = {}
                    errsByUser[user]['errors'][errcode]['error'] = errcode
                    errsByUser[user]['errors'][errcode]['codename'] = err['error']
                    errsByUser[user]['errors'][errcode]['codeval'] = job[err['error']]
                    errsByUser[user]['errors'][errcode]['diag'] = errdiag
                    errsByUser[user]['errors'][errcode]['count'] = 0
                errsByUser[user]['errors'][errcode]['count'] += 1
                errsByUser[user]['toterrors'] += 1

                if site not in errsBySite:
                    errsBySite[site] = {}
                    errsBySite[site]['name'] = site
                    errsBySite[site]['errors'] = {}
                    errsBySite[site]['toterrors'] = 0
                if errcode not in errsBySite[site]['errors']:
                    errsBySite[site]['errors'][errcode] = {}
                    errsBySite[site]['errors'][errcode]['error'] = errcode
                    errsBySite[site]['errors'][errcode]['codename'] = err['error']
                    errsBySite[site]['errors'][errcode]['codeval'] = job[err['error']]
                    errsBySite[site]['errors'][errcode]['diag'] = errdiag
                    errsBySite[site]['errors'][errcode]['count'] = 0
                errsBySite[site]['errors'][errcode]['count'] += 1
                errsBySite[site]['toterrors'] += 1
                
                if tasktype == 'jeditaskid' or taskid > 1000000 or 'produsername' in request.GET:
                    if taskid not in errsByTask:
                        errsByTask[taskid] = {}
                        errsByTask[taskid]['name'] = taskid
                        errsByTask[taskid]['errors'] = {}
                        errsByTask[taskid]['toterrors'] = 0
                        errsByTask[taskid]['tasktype'] = tasktype
                    if errcode not in errsByTask[taskid]['errors']:
                        errsByTask[taskid]['errors'][errcode] = {}
                        errsByTask[taskid]['errors'][errcode]['error'] = errcode
                        errsByTask[taskid]['errors'][errcode]['codename'] = err['error']
                        errsByTask[taskid]['errors'][errcode]['codeval'] = job[err['error']]
                        errsByTask[taskid]['errors'][errcode]['diag'] = errdiag
                        errsByTask[taskid]['errors'][errcode]['count'] = 0
                    errsByTask[taskid]['errors'][errcode]['count'] += 1
                    errsByTask[taskid]['toterrors'] += 1
                
    ## reorganize as sorted lists
    errsByCountL = []
    errsBySiteL = []
    errsByUserL = []
    errsByTaskL = []
    
    kys = errsByCount.keys()
    kys.sort()
    for err in kys:
        errsByCountL.append(errsByCount[err])
    if 'sortby' in request.GET and request.GET['sortby'] == 'count':
        errsByCountL = sorted(errsByCountL, key=lambda x:-x['count'])

    kys = errsByUser.keys()
    kys.sort()
    for user in kys:
        errsByUser[user]['errorlist'] = []
        errkeys = errsByUser[user]['errors'].keys()
        errkeys.sort()
        for err in errkeys:
            errsByUser[user]['errorlist'].append(errsByUser[user]['errors'][err])
        errsByUserL.append(errsByUser[user])
    if 'sortby' in request.GET and request.GET['sortby'] == 'count':
        errsByUserL = sorted(errsByUserL, key=lambda x:-x['toterrors'])

    kys = errsBySite.keys()
    kys.sort()
    for site in kys:
        errsBySite[site]['errorlist'] = []
        errkeys = errsBySite[site]['errors'].keys()
        errkeys.sort()
        for err in errkeys:
            errsBySite[site]['errorlist'].append(errsBySite[site]['errors'][err])
        errsBySiteL.append(errsBySite[site])
    if 'sortby' in request.GET and request.GET['sortby'] == 'count':
        errsBySiteL = sorted(errsBySiteL, key=lambda x:-x['toterrors'])

    kys = errsByTask.keys()
    kys.sort()
    for taskid in kys:
        errsByTask[taskid]['errorlist'] = []
        errkeys = errsByTask[taskid]['errors'].keys()
        errkeys.sort()
        for err in errkeys:
            errsByTask[taskid]['errorlist'].append(errsByTask[taskid]['errors'][err])
        errsByTaskL.append(errsByTask[taskid])
    if 'sortby' in request.GET and request.GET['sortby'] == 'count':
        errsByTaskL = sorted(errsByTaskL, key=lambda x:-x['toterrors'])

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

    if 'sortby' in request.GET and request.GET['sortby'] == 'count':
        for item in suml:
            item['list'] = sorted(item['list'], key=lambda x:-x['kvalue'])

    kys = errHist.keys()
    kys.sort()
    errHistL = []
    for k in kys:
        errHistL.append( [ k, errHist[k] ] )

    return errsByCountL, errsBySiteL, errsByUserL, errsByTaskL, suml, errHistL

def errorSummary(request):
    if 'sortby' in request.GET:
        sortby = request.GET['sortby']
    else:
        sortby = 'alpha'
    query = setupView(request, hours=12, limit=3000)
    query['jobstatus__in'] = [ 'failed', 'holding' ]
    jobtype = ''
    if 'jobtype' in request.GET:
        jobtype = request.GET['jobtype']
    elif '/analysis' in request.path:
        jobtype = 'analysis'
    elif '/production' in request.path:
        jobtype = 'production'
    jobs = []
    values = 'produsername', 'pandaid', 'cloud','computingsite','cpuconsumptiontime','jobstatus','transformation','prodsourcelabel','specialhandling','vo','modificationtime', 'atlasrelease', 'jobsetid', 'processingtype', 'workinggroup', 'jeditaskid', 'taskid', 'starttime', 'endtime', 'brokerageerrorcode', 'brokerageerrordiag', 'ddmerrorcode', 'ddmerrordiag', 'exeerrorcode', 'exeerrordiag', 'jobdispatchererrorcode', 'jobdispatchererrordiag', 'piloterrorcode', 'piloterrordiag', 'superrorcode', 'superrordiag', 'taskbuffererrorcode', 'taskbuffererrordiag', 'transexitcode', 'destinationse', 'currentpriority', 'computingelement'
    jobs.extend(Jobsdefined4.objects.filter(**query)[:JOB_LIMIT].values(*values))
    jobs.extend(Jobsactive4.objects.filter(**query)[:JOB_LIMIT].values(*values))
    jobs.extend(Jobswaiting4.objects.filter(**query)[:JOB_LIMIT].values(*values))
    jobs.extend(Jobsarchived4.objects.filter(**query)[:JOB_LIMIT].values(*values))
    jobs.extend(Jobsarchived.objects.filter(**query)[:JOB_LIMIT].values(*values))
    jobs = cleanJobList(jobs)
    njobs = len(jobs)
    errsByCount, errsBySite, errsByUser, errsByTask, sumd, errHist = errorSummaryDict(request,jobs)
    if request.META.get('CONTENT_TYPE', 'text/plain') == 'text/plain':
        nosorturl = removeParam(request.get_full_path(), 'sortby')
        xurl = extensibleURL(request)
        data = {
            'prefix': getPrefix(request),
            'viewParams' : viewParams,
            'requestParams' : request.GET,
            'requestString' : request.META['QUERY_STRING'],
            'jobtype' : jobtype,
            'njobs' : njobs,
            'hours' : LAST_N_HOURS_MAX,
            'limit' : JOB_LIMIT,
            'user' : None,
            'xurl' : xurl,
            'nosorturl' : nosorturl,
            'errsByCount' : errsByCount,
            'errsBySite' : errsBySite,
            'errsByUser' : errsByUser,
            'errsByTask' : errsByTask,
            'sumd' : sumd,
            'errHist' : errHist,
            'tfirst' : TFIRST,
            'tlast' : TLAST,
            'sortby' : sortby,
        }
        data.update(getContextVariables(request))
        return render_to_response('errorSummary.html', data, RequestContext(request))
    elif request.META.get('CONTENT_TYPE', 'text/plain') == 'application/json':
        resp = []
        for job in jobs:
            resp.append({ 'pandaid': job.pandaid, 'status': job.jobstatus, 'prodsourcelabel': job.prodsourcelabel, 'produserid' : job.produserid})
        return  HttpResponse(json_dumps(resp), mimetype='text/html')

def removeParam(urlquery, parname, mode='complete'):
    """Remove a parameter from current query"""
    urlquery = urlquery.replace('&&','&')
    urlquery = urlquery.replace('?&','?')
    pstr = '.*(%s=[a-zA-Z0-9\.\-]*).*' % parname
    pat = re.compile(pstr)
    mat = pat.match(urlquery)
    if mat:
        pstr = mat.group(1)
        urlquery = urlquery.replace(pstr,'')
        urlquery = urlquery.replace('&&','&')
        urlquery = urlquery.replace('?&','?')
        if mode != 'extensible':
            if urlquery.endswith('?') or urlquery.endswith('&'): urlquery = urlquery[:len(urlquery)-1]
    return urlquery

def incidentList(request):
    if 'hours' not in request.GET:
        hours = 24*3
    else:
        hours = int(request.GET['hours'])
    setupView(request, hours=hours, limit=9999999)
    iquery = {}
    startdate = datetime.utcnow() - timedelta(hours=hours)
    startdate = startdate.strftime(defaultDatetimeFormat)
    enddate = datetime.utcnow().strftime(defaultDatetimeFormat)
    iquery['at_time__range'] = [startdate, enddate]
    if 'site' in request.GET:
        iquery['description__contains'] = 'queue=%s' % request.GET['site']
    if 'category' in request.GET:
        iquery['description__startswith'] = '%s:' % request.GET['category']
    if 'comment' in request.GET:
        iquery['description__contains'] = '%s' % request.GET['comment']
    if 'notifier' in request.GET:
        iquery['description__contains'] = 'DN=%s' % request.GET['notifier']
    incidents = Incidents.objects.filter(**iquery).order_by('at_time').reverse().values()
    sumd = {}
    pars = {}
    incHist = {}
    for inc in incidents:
        desc = inc['description']
        desc = desc.replace('&nbsp;',' ')
        parsmat = re.match('^([a-z\s]+):\s+queue=([^\s]+)\s+DN=(.*)\s\s\s*([A-Za-z^ \.0-9]*)$',desc)
        tm = inc['at_time']
        tm = tm - timedelta(minutes=tm.minute % 30, seconds=tm.second, microseconds=tm.microsecond)
        if not tm in incHist: incHist[tm] = 0
        incHist[tm] += 1
        if parsmat:
            pars['category'] = parsmat.group(1)
            pars['site'] = parsmat.group(2)
            pars['notifier'] = parsmat.group(3)
            pars['type'] = inc['typekey']
            if parsmat.group(4): pars['comment'] = parsmat.group(4)
        else:
            parsmat = re.match('^([A-Za-z\s]+):.*$',desc)
            if parsmat:
                pars['category'] = parsmat.group(1)
            else:
                pars['category'] = desc[:10]
        for p in pars:
            if p not in sumd:
                sumd[p] = {}
                sumd[p]['param'] = p
                sumd[p]['vals'] = {}
            if pars[p] not in sumd[p]['vals']:
                sumd[p]['vals'][pars[p]] = {}
                sumd[p]['vals'][pars[p]]['name'] = pars[p]
                sumd[p]['vals'][pars[p]]['count'] = 0
            sumd[p]['vals'][pars[p]]['count'] += 1
        ## convert incident components to URLs. Easier here than in the template.
        if 'site' in pars:
            inc['description'] = re.sub('queue=[^\s]+','queue=<a href="%ssite=%s">%s</a>' % (extensibleURL(request), pars['site'], pars['site']), inc['description'])

    ## convert to ordered lists
    suml = []
    for p in sumd:
        itemd = {}
        itemd['param'] = p
        iteml = []
        kys = sumd[p]['vals'].keys()
        kys.sort(key=lambda y: y.lower())
        for ky in kys:
            iteml.append({ 'kname' : ky, 'kvalue' : sumd[p]['vals'][ky]['count'] })
        itemd['list'] = iteml
        suml.append(itemd)
    suml = sorted(suml, key=lambda x:x['param'].lower())

    kys = incHist.keys()
    kys.sort()
    incHistL = []
    for k in kys:
        incHistL.append( [ k, incHist[k] ] )

    if request.META.get('CONTENT_TYPE', 'text/plain') == 'text/plain':
        data = {
            'viewParams' : viewParams,
            'requestParams' : request.GET,
            'user' : None,
            'incidents': incidents,
            'sumd' : suml,
            'incHist' : incHistL,
            'xurl' : extensibleURL(request),
            'hours' : hours,
            'ninc' : len(incidents),
        }
        return render_to_response('incidents.html', data, RequestContext(request))
    elif request.META.get('CONTENT_TYPE', 'text/plain') == 'application/json':
        resp = incidents
        return  HttpResponse(json_dumps(resp), mimetype='text/html')

def pandaLogger(request):
    if 'hours' not in request.GET:
        hours = 12
    else:
        hours = int(request.GET['hours'])
    setupView(request, hours=hours, limit=9999999)
    iquery = {}
    startdate = datetime.utcnow() - timedelta(hours=hours)
    startdate = startdate.strftime(defaultDatetimeFormat)
    enddate = datetime.utcnow().strftime(defaultDatetimeFormat)
    iquery['bintime__range'] = [startdate, enddate]
    getrecs = False
    if 'category' in request.GET:
        iquery['name'] = request.GET['category']
        getrecs = True
    if 'type' in request.GET:
        iquery['type'] = request.GET['type']
        getrecs = True
    if 'level' in request.GET:
        iquery['levelname'] = request.GET['level'].upper()
        getrecs = True
    if 'taskid' in request.GET:
        iquery['message__startswith'] = request.GET['taskid']
        getrecs = True
    if 'site' in request.GET:
        iquery['message__startswith'] = request.GET['site']
        getrecs = True
    if 'pandaid' in request.GET:
        iquery['pid'] = request.GET['pandaid']
        getrecs = True
    counts = Pandalog.objects.filter(**iquery).values('name','type','levelname').annotate(Count('levelname')).order_by('name','type','levelname')
    if getrecs:
        records = Pandalog.objects.filter(**iquery).order_by('bintime').reverse()[:JOB_LIMIT].values()
        ## histogram of logs vs. time, for plotting
        logHist = {}
        for r in records:
            r['levelname'] = r['levelname'].lower()
            tm = r['bintime']
            tm = tm - timedelta(minutes=tm.minute % 30, seconds=tm.second, microseconds=tm.microsecond)
            if not tm in logHist: logHist[tm] = 0
            logHist[tm] += 1
        kys = logHist.keys()
        kys.sort()
        logHistL = []
        for k in kys:
            logHistL.append( [ k, logHist[k] ] )
    else:
        records = None
        logHistL = None
    logs = {}
    totcount = 0
    for inc in counts:
        name = inc['name']
        type = inc['type']
        level = inc['levelname']
        count = inc['levelname__count']
        totcount += count
        if name not in logs:
            logs[name] = {}
            logs[name]['name'] = name
            logs[name]['count'] = 0
            logs[name]['types'] = {}
        logs[name]['count'] += count
        if type not in logs[name]['types']:
            logs[name]['types'][type] = {}
            logs[name]['types'][type]['name'] = type
            logs[name]['types'][type]['count'] = 0
            logs[name]['types'][type]['levels'] = {}
        logs[name]['types'][type]['count'] += count
        if level not in logs[name]['types'][type]['levels']:
            logs[name]['types'][type]['levels'][level] = {}
            logs[name]['types'][type]['levels'][level]['name'] = level.lower()
            logs[name]['types'][type]['levels'][level]['count'] = 0
        logs[name]['types'][type]['levels'][level]['count'] += count

    ## convert to ordered lists
    logl = []
    for l in logs:
        itemd = {}
        itemd['name'] = logs[l]['name']
        itemd['types'] = []
        for t in logs[l]['types']:
            logs[l]['types'][t]['levellist'] = []
            for v in logs[l]['types'][t]['levels']:
                logs[l]['types'][t]['levellist'].append(logs[l]['types'][t]['levels'][v])
            logs[l]['types'][t]['levellist'] = sorted(logs[l]['types'][t]['levellist'], key=lambda x:x['name'])
            typed = {}
            typed['name'] = logs[l]['types'][t]['name']
            itemd['types'].append(logs[l]['types'][t])
        itemd['types'] = sorted(itemd['types'], key=lambda x:x['name'])
        logl.append(itemd)
    logl = sorted(logl, key=lambda x:x['name'])

    if request.META.get('CONTENT_TYPE', 'text/plain') == 'text/plain':
        data = {
            'viewParams' : viewParams,
            'requestParams' : request.GET,
            'user' : None,
            'logl' : logl,
            'records' : records,
            'ninc' : totcount,
            'logHist' : logHistL,
            'xurl' : extensibleURL(request),
            'hours' : hours,
        }
        return render_to_response('pandaLogger.html', data, RequestContext(request))
    elif request.META.get('CONTENT_TYPE', 'text/plain') == 'application/json':
        resp = incidents
        return  HttpResponse(json_dumps(resp), mimetype='text/html')

def workingGroups(request):
    if dbaccess['default']['ENGINE'].find('oracle') >= 0:
        VOMODE = 'atlas'
    else:
        VOMODE = ''
    if VOMODE != 'atlas':
        hours = 24*7
    else:
        hours = 24
    query = setupView(request,hours=hours,limit=999999)
    query['workinggroup__isnull'] = False
    wgsummarydata = wgSummary(query)
    wgs = {}
    for rec in wgsummarydata:
        wg = rec['workinggroup']
        if wg == None: continue
        jobstatus = rec['jobstatus']
        count = rec['jobstatus__count']
        if wg not in wgs:
            wgs[wg] = {}
            wgs[wg]['name'] = wg
            wgs[wg]['count'] = 0
            wgs[wg]['states'] = {}
            wgs[wg]['statelist'] = []
            for state in statelist:
                wgs[wg]['states'][state] = {}
                wgs[wg]['states'][state]['name'] = state
                wgs[wg]['states'][state]['count'] = 0
        wgs[wg]['count'] += count
        wgs[wg]['states'][jobstatus]['count'] += count

    errthreshold = 15
    ## Convert dict to summary list
    wgkeys = wgs.keys()
    wgkeys.sort()
    wgsummary = []
    for wg in wgkeys:
        for state in statelist:
            wgs[wg]['statelist'].append(wgs[wg]['states'][state])
            if int(wgs[wg]['states']['finished']['count']) + int(wgs[wg]['states']['failed']['count']) > 0:
                wgs[wg]['pctfail'] = int(100.*float(wgs[wg]['states']['failed']['count'])/(wgs[wg]['states']['finished']['count']+wgs[wg]['states']['failed']['count']))

        wgsummary.append(wgs[wg])
    if len(wgsummary) == 0: wgsummary = None

    if request.META.get('CONTENT_TYPE', 'text/plain') == 'text/plain':
        xurl = extensibleURL(request)
        data = {
            'viewParams' : viewParams,
            'requestParams' : request.GET,
            'url' : request.path,
            'xurl' : xurl,
            'user' : None,
            'wgsummary' : wgsummary,
            'hours' : hours,
            'errthreshold' : errthreshold,
        }
        return render_to_response('workingGroups.html', data, RequestContext(request))
    elif request.META.get('CONTENT_TYPE', 'text/plain') == 'application/json':
        resp = []
        return  HttpResponse(json_dumps(resp), mimetype='text/html')

def datasetInfo(request):
    setupView(request, hours=365*24, limit=999999999)
    query = {}
    dsets = []
    dsrec = None
    colnames = []
    columns = []
    if 'datasetname' in request.GET:
        dataset = request.GET['datasetname']
        query['datasetname'] = request.GET['datasetname']
    elif 'datasetid' in request.GET:
        dataset = request.GET['datasetid']
        query['datasetid'] = request.GET['datasetid']
    else:
        dataset = None
    
    if dataset:
        dsets = JediDatasets.objects.filter(**query).values()
        if len(dsets) == 0:
            startdate = datetime.utcnow() - timedelta(hours=30*24)
            startdate = startdate.strftime(defaultDatetimeFormat)
            enddate = datetime.utcnow().strftime(defaultDatetimeFormat)
            query = { 'modificationdate__range' : [startdate, enddate] }
            if 'datasetname' in request.GET:
                query['name'] = request.GET['datasetname']
            elif 'datasetid' in request.GET:
                query['vuid'] = request.GET['datasetid']
            moredsets = Datasets.objects.filter(**query).values()
            if len(moredsets) > 0:
                dsets = moredsets
                for ds in dsets:
                    ds['datasetname'] = ds['name']
                    ds['creationtime'] = ds['creationdate']
                    ds['modificationtime'] = ds['modificationdate']
                    ds['nfiles'] = ds['numberfiles']
                    ds['datasetid'] = ds['vuid']
    if len(dsets) > 0:
        dsrec = dsets[0]
        dataset = dsrec['datasetname']
        colnames = dsrec.keys()
        colnames.sort()
        for k in colnames:
            val = dsrec[k]
            if dsrec[k] == None:
                val = ''
                continue
            pair = { 'name' : k, 'value' : val }
            columns.append(pair)

    if request.META.get('CONTENT_TYPE', 'text/plain') == 'text/plain':
        data = {
            'viewParams' : viewParams,
            'requestParams' : request.GET,
            'dsrec' : dsrec,
            'datasetname' : dataset,
            'columns' : columns,
        }
        data.update(getContextVariables(request))
        return render_to_response('datasetInfo.html', data, RequestContext(request))
    elif request.META.get('CONTENT_TYPE', 'text/plain') == 'application/json':
        return  HttpResponse(json_dumps(dsrec), mimetype='text/html')

def datasetList(request):
    setupView(request, hours=365*24, limit=999999999)
    query = {}
    dsets = []
    if 'jeditaskid' in request.GET:
        query['jeditaskid'] = request.GET['jeditaskid']
    
    if len(query) > 0:
        dsets = JediDatasets.objects.filter(**query).values()

    if request.META.get('CONTENT_TYPE', 'text/plain') == 'text/plain':
        data = {
            'viewParams' : viewParams,
            'requestParams' : request.GET,
            'datasets' : dsets,
        }
        data.update(getContextVariables(request))
        return render_to_response('datasetList.html', data, RequestContext(request))
    elif request.META.get('CONTENT_TYPE', 'text/plain') == 'application/json':
        return  HttpResponse(json_dumps(dsrec), mimetype='text/html')

def fileInfo(request):
    setupView(request, hours=365*24, limit=999999999)
    query = {}
    files = []
    frec = None
    colnames = []
    columns = []
    if 'filename' in request.GET:
        file = request.GET['filename']
        query['lfn'] = request.GET['filename']
    elif 'lfn' in request.GET:
        file = request.GET['lfn']
        query['lfn'] = request.GET['lfn']
    elif 'fileid' in request.GET:
        file = request.GET['fileid']
        query['fileid'] = request.GET['fileid']
    elif 'guid' in request.GET:
        file = request.GET['guid']
        query['guid'] = request.GET['guid']
    else:
        file = None
    if 'scope' in request.GET:
        query['scope'] = request.GET['scope']
    if 'pandaid' in request.GET and request.GET['pandaid'] != '':
        query['pandaid'] = request.GET['pandaid']
    
    if file:
        files = JediDatasetContents.objects.filter(**query).values()
        if len(files) == 0:
            morefiles = Filestable4.objects.filter(**query).values()
            if len(morefiles) == 0:
                morefiles.extend(FilestableArch.objects.filter(**query).values())
            if len(morefiles) > 0:
                files = morefiles
                for f in files:
                    f['creationdate'] = f['modificationtime']
                    f['fileid'] = f['row_id']
                    f['datasetname'] = f['dataset']

        for f in files:
            f['fsizemb'] = "%0.2f" % (f['fsize']/1000000.)
            dsets = JediDatasets.objects.filter(datasetid=f['datasetid']).values()
            if len(dsets) > 0:
                f['datasetname'] = dsets[0]['datasetname']

    if len(files) > 0:
        frec = files[0]
        file = frec['lfn']
        colnames = frec.keys()
        colnames.sort()
        for k in colnames:
            val = frec[k]
            if frec[k] == None:
                val = ''
                continue
            pair = { 'name' : k, 'value' : val }
            columns.append(pair)

    if request.META.get('CONTENT_TYPE', 'text/plain') == 'text/plain':
        data = {
            'viewParams' : viewParams,
            'requestParams' : request.GET,
            'frec' : frec,
            'filename' : file,
            'columns' : columns,
        }
        data.update(getContextVariables(request))
        return render_to_response('fileInfo.html', data, RequestContext(request))
    elif request.META.get('CONTENT_TYPE', 'text/plain') == 'application/json':
        return  HttpResponse(json_dumps(dsrec), mimetype='text/html')

def fileList(request):
    setupView(request, hours=365*24, limit=999999999)
    query = {}
    files = []
    frec = None
    colnames = []
    columns = []
    datasetname = ''
    datasetid = 0
    if 'datasetname' in request.GET:
        datasetname = request.GET['datasetname']
        dsets = JediDatasets.objects.filter(datasetname=datasetname).values()
        if len(dsets) > 0:
            datasetid = dsets[0]['datasetid']
    elif 'datasetid' in request.GET:
        datasetid = request.GET['datasetid']
        dsets = JediDatasets.objects.filter(datasetid=datasetid).values()
        if len(dsets) > 0:
            datasetname = dsets[0]['datasetname']

    files = []
    if datasetid > 0:
        query['datasetid'] = datasetid
        files = JediDatasetContents.objects.filter(**query).values()
        for f in files:
            f['fsizemb'] = "%0.2f" % (f['fsize']/1000000.)

    if request.META.get('CONTENT_TYPE', 'text/plain') == 'text/plain':
        data = {
            'viewParams' : viewParams,
            'requestParams' : request.GET,
            'files' : files,
        }
        data.update(getContextVariables(request))
        return render_to_response('fileList.html', data, RequestContext(request))
    elif request.META.get('CONTENT_TYPE', 'text/plain') == 'application/json':
        return  HttpResponse(json_dumps(files), mimetype='text/html')

def workQueues(request):
    setupView(request, hours=180*24, limit=9999999)
    query = {}
    for param in request.GET:
        for field in JediWorkQueue._meta.get_all_field_names():
            if param == field:
                query[param] = request.GET[param]
    queues = JediWorkQueue.objects.filter(**query).order_by('queue_type','queue_order').values()
    #queues = sorted(queues, key=lambda x:x['queue_name'],reverse=True)
        
    if request.META.get('CONTENT_TYPE', 'text/plain') == 'text/plain':
        data = {
            'viewParams' : viewParams,
            'requestParams' : request.GET,
            'queues': queues,
            'xurl' : extensibleURL(request),
        }
        return render_to_response('workQueues.html', data, RequestContext(request))
    elif request.META.get('CONTENT_TYPE', 'text/plain') == 'application/json':
        return  HttpResponse(json_dumps(queues), mimetype='text/html')

