"""
    pandajob.utils
"""
import pytz
from datetime import datetime, timedelta

from django.conf import settings

from ..common.settings import defaultDatetimeFormat
from ..common.models import JediJobRetryHistory
from ..common.models import Users

from ..resource.models import Schedconfig

from .models import Jobsactive4, Jobsdefined4, Jobswaiting4, \
    Jobsarchived4


homeCloud = {}
statelist = [ 'defined', 'waiting', 'assigned', 'activated', 'sent', \
             'running', 'holding', 'finished', 'failed', 'cancelled', \
             'transferring', 'starting', 'pending' ]
sitestatelist = [ 'assigned', 'activated', 'sent', 'starting', 'running', \
                 'holding', 'transferring', 'finished', 'failed', 'cancelled' ]
viewParams = {}
VOLIST = [ 'atlas', 'bigpanda', 'htcondor', 'lsst' ]
VONAME = { 'atlas' : 'ATLAS', \
           'bigpanda' : 'BigPanDA', \
           'htcondor' : 'HTCondor', \
           'lsst' : 'LSST', \
           '' : '' \
}
VOMODE = ' '
standard_fields = [ 'processingtype', 'computingsite', 'destinationse', \
                   'jobstatus', 'prodsourcelabel', 'produsername', \
                   'jeditaskid', 'taskid', 'workinggroup', 'transformation', \
                   'vo', 'cloud']
standard_sitefields = [ 'region', 'gocname', 'status', 'tier', '\
                        comment_field', 'cloud' ]
standard_taskfields = [ 'tasktype', 'status', 'corecount', 'taskpriority', \
                       'username', 'transuses', 'transpath', 'workinggroup', \
                       'processingtype', 'cloud', ]
LAST_N_HOURS_MAX = 0
#JOB_LIMIT = 0
JOB_LIMIT = 1000


def setupHomeCloud():
    global homeCloud
    if len(homeCloud) > 0:
        return
    sites = Schedconfig.objects.filter().exclude(cloud='CMS').values()
    for site in sites:
        homeCloud[site['siteid']] = site['cloud']


def cleanJobList(jobs, mode='drop'):
    for job in jobs:
        if not job['produsername']:
            if job['produserid']:
                job['produsername'] = job['produserid']
            else:
                job['produsername'] = 'Unknown'
        if job['transformation']: job['transformation'] = job['transformation'].split('/')[-1]
        if job['jobstatus'] == 'failed':
            job['errorinfo'] = errorInfo(job, nchars=50)
        else:
            job['errorinfo'] = ''
        job['jobinfo'] = ''
        if isEventService(job): job['jobinfo'] = 'Event service job'

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
                    print 'dropping', pandaid
                    dropJob = retry['newpandaid']
            if dropJob == 0:
                newjobs.append(job)
            else:
                droplist.append({ 'pandaid' : pandaid, 'newpandaid' : dropJob })
        droplist = sorted(droplist, key=lambda x:-x['pandaid'])
        jobs = newjobs
    jobs = sorted(jobs, key=lambda x:-x['pandaid'])
    return jobs


def cleanTaskList(tasks):
    for task in tasks:
        if task['transpath']: task['transpath'] = task['transpath'].split('/')[-1]
    return tasks


def siteSummaryDict(sites):
    """ Return a dictionary summarizing the field values for the chosen most interesting fields """
    global standard_sitefields
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
        if (site['multicloud'] is not None) and (site['multicloud'] != 'None') and (re.match('[A-Z]+', site['multicloud'])):
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
                sumd[user]['n' + state] = 0
            sumd[user]['nsites'] = 0
            sumd[user]['sites'] = {}
            sumd[user]['nclouds'] = 0
            sumd[user]['clouds'] = {}
            sumd[user]['nqueued'] = 0
#            sumd[user]['latest'] = timezone.now() - timedelta(hours=2400)
            sumd[user]['latest'] = datetime.utcnow().replace(tzinfo=pytz.utc) - timedelta(hours=2400)
            sumd[user]['pandaid'] = 0
        cloud = job['cloud']
        site = job['computingsite']
        cpu = float(job['cpuconsumptiontime']) / 1.
        state = job['jobstatus']
        if job['modificationtime'] > sumd[user]['latest']: sumd[user]['latest'] = job['modificationtime']
        if job['pandaid'] > sumd[user]['pandaid']: sumd[user]['pandaid'] = job['pandaid']
        sumd[user]['cputime'] += cpu
        sumd[user]['njobs'] += 1
        sumd[user]['n' + state] += 1
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


def errorInfo(job, nchars=300):
    errtxt = ''
    if int(job['brokerageerrorcode']) != 0:
        errtxt += 'Brokerage error %s: %s <br>' % (job['brokerageerrorcode'], job['brokerageerrordiag'])
    if int(job['ddmerrorcode']) != 0:
        errtxt += 'DDM error %s: %s <br>' % (job['ddmerrorcode'], job['ddmerrordiag'])
    if int(job['exeerrorcode']) != 0:
        errtxt += 'Executable error %s: %s <br>' % (job['exeerrorcode'], job['exeerrordiag'])
    if int(job['jobdispatchererrorcode']) != 0:
        errtxt += 'Dispatcher error %s: %s <br>' % (job['jobdispatchererrorcode'], job['jobdispatchererrordiag'])
    if int(job['piloterrorcode']) != 0:
        errtxt += 'Pilot error %s: %s <br>' % (job['piloterrorcode'], job['piloterrordiag'])
    if int(job['superrorcode']) != 0:
        errtxt += 'Sup error %s: %s <br>' % (job['superrorcode'], job['superrordiag'])
    if int(job['taskbuffererrorcode']) != 0:
        errtxt += 'Task buffer error %s: %s <br>' % (job['taskbuffererrorcode'], job['taskbuffererrordiag'])
    if job['transexitcode'] != '' and job['transexitcode'] is not None and int(job['transexitcode']) > 0:
        errtxt += 'Transformation exit code %s' % job['transexitcode']
    if len(errtxt) > nchars:
        ret = errtxt[:nchars] + '...'
    else:
        ret = errtxt[:nchars]
    return ret


def isEventService(job):
    if job is not None and 'specialhandling' in job \
        and job['specialhandling'] is not None \
        and job['specialhandling'].find('eventservice') >= 0:
        return True
    else:
        return False


def siteSummary(query):
    summary = []
    summary.extend(Jobsactive4.objects.filter(**query).values('cloud', 'computingsite', 'jobstatus').annotate(Count('jobstatus')).order_by('cloud', 'computingsite', 'jobstatus'))
    summary.extend(Jobsarchived4.objects.filter(**query).values('cloud', 'computingsite', 'jobstatus').annotate(Count('jobstatus')).order_by('cloud', 'computingsite', 'jobstatus'))
    return summary


def voSummary(query):
    summary = []
    summary.extend(Jobsactive4.objects.filter(**query).values('vo', 'jobstatus').annotate(Count('jobstatus')))
    summary.extend(Jobsarchived4.objects.filter(**query).values('vo', 'jobstatus').annotate(Count('jobstatus')))
    return summary


def wnSummary(query):
    summary = []
    summary.extend(Jobsactive4.objects.filter(**query).values('cloud', 'computingsite', 'modificationhost', 'jobstatus').annotate(Count('jobstatus')))
    summary.extend(Jobsarchived4.objects.filter(**query).values('cloud', 'computingsite', 'modificationhost', 'jobstatus').annotate(Count('jobstatus')))
    return summary


def jobStateSummary(jobs):
    global statelist
    statecount = {}
    for state in statelist:
        statecount[state] = 0
    for job in jobs:
        statecount[job['jobstatus']] += 1
    return statecount


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
    jobs.extend(Jobsdefined4.objects.filter(**query).values('pandaid', 'jobstatus', 'jeditaskid'))
    jobs.extend(Jobswaiting4.objects.filter(**query).values('pandaid', 'jobstatus', 'jeditaskid'))
    jobs.extend(Jobsactive4.objects.filter(**query).values('pandaid', 'jobstatus', 'jeditaskid'))
    jobs.extend(Jobsarchived4.objects.filter(**query).values('pandaid', 'jobstatus', 'jeditaskid'))
    jobs.extend(Jobsarchived.objects.filter(**query).values('pandaid', 'jobstatus', 'jeditaskid'))

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


