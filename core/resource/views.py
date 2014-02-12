# Create your views here.

import datetime
import json
import logging
import pycurl
import pytz
import StringIO
import time
import warnings

warnings.filterwarnings(
        'error', r"DateTimeField received a naive datetime",
        RuntimeWarning, r'django\.db\.models\.fields')
#
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from django.core.exceptions import ObjectDoesNotExist
#
from ..topology.models import Schedconfig
from ..settings import SOURCE_SCHEDCONFIG
from ..core.utils import getPrefix
from ..core.utils import getPrefix, getContextVariables

_logger = logging.getLogger(__name__)

#currentDateFormat = "%Y-%m-%d %H:%M:%S%z"
currentDateFormat = "%Y-%m-%d %H:%M:%SZ"
#lastmodDateFormat = "%Y-%m-%dT%H:%M:%S.%f %z"
lastmodDateFormat = "%Y-%m-%dT%H:%M:%S.%f"

def downloadSchedconfigJson(url, buf):

    localBuffer = StringIO.StringIO()
    
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.CONNECTTIMEOUT, 60)
    c.setopt(c.TIMEOUT, 120)
    c.setopt(c.VERBOSE, False)
#    c.setopt(c.SSLCERT, '/data/sitestatusboard/scripts/SITE_EXCLUSION/certs/hostcert.pem')
#    c.setopt(c.SSLKEY, '/data/sitestatusboard/scripts/SITE_EXCLUSION/certs/hostkey.pem')
#    c.setopt(c.CAINFO, '/data/sitestatusboard/scripts/SITE_EXCLUSION/CERN_CA_all.pem')
    c.setopt(c.SSL_VERIFYPEER, 0)
    c.setopt(c.SSL_VERIFYHOST, 0)
    c.setopt(c.WRITEFUNCTION, localBuffer.write)
    try:
        c.perform()
        buf.write(localBuffer.getvalue())
    except pycurl.error, e:
        errno, errstr = e
        fail_counter_max = 5
        fail_counter = 1
        _logger.error(u'Attempt %d errno: %s errstr: %s with URL %s' % (fail_counter, errno, errstr, url))
        
        time.sleep(2)
        
        for x in xrange(fail_counter_max):
            if fail_counter < fail_counter_max:
                try:
                    c.perform()
                    buf.write(localBuffer.getvalue())
                except pycurl.error, e:
                    errno, errstr = e
                    _logger.error(u'Attempt %d errno: %s errstr: %s with URL %s' % (fail_counter, errno, errstr, url))
                    time.sleep(2)
    
    return localBuffer.getvalue()


def getResultString(nickname, diffDict, action="Updated"):
    result = "%(action)s schedconfig info for queue %(nickname)s.\n" % \
        {'action': action, 'nickname': nickname}
    keys = diffDict.keys()
    for key in keys:
        result += "%(key)s: %(old)s --> %(new)s" % \
            {'key': key, 'old': diffDict[key]['old'], 'new': diffDict[key]['new']}
    return result


def updateSchedconfig(request, vo):
    _logger.debug('VO: ...%s...' % vo)
    currentDate = datetime.datetime.utcnow().replace(tzinfo=pytz.utc).strftime(currentDateFormat)
#    SOURCE_SCHEDCONFIG
    schedconfigFile = StringIO.StringIO()
    schedconfigFileContent = ""
    result = []
    if vo in SOURCE_SCHEDCONFIG:
#        schedconfigFile =
        schedconfigFileContent = downloadSchedconfigJson(SOURCE_SCHEDCONFIG[vo], schedconfigFile)
    else:
        result.append({'msg': "WARNING Cannot find schedconfig source URL for VO '%(vo)s'. Available VOs: %(schedVO)s.\n" % \
                            {'vo': vo, 'schedVO': SOURCE_SCHEDCONFIG.keys()}
                      })
#        result+="WARNING " + "Cannot find schedconfig source URL for VO '%(vo)s'. Available VOs: %(schedVO)s.\n" % \
#            {'vo': vo, 'schedVO': SOURCE_SCHEDCONFIG.keys()}

    if len(schedconfigFileContent) > 0:
        schedconfigData = {}
        try:
            schedconfigData = json.loads(schedconfigFile.getvalue())
        except:
            raise
        _logger.debug('type(schedconfigData)=' + str(type(schedconfigData)))
        _logger.debug('schedconfigData.keys()=' + str(schedconfigData.keys()))
        schedconfigQueues = schedconfigData.keys()
        schedconfigQueuesList = []
        for schedconfigQueue in schedconfigQueues:
            nickname = schedconfigData[schedconfigQueue]["nickname"]
            schedconfigQueuesList.append(nickname)
            _logger.debug('nickname=%s data=%s' % (nickname, schedconfigData[schedconfigQueue]))
            lastmod = schedconfigData[schedconfigQueue]["lastmod"]
            try:
                ###  "2013-06-06T10:51:24.111010"
                lastmod = datetime.datetime.strptime(lastmod, lastmodDateFormat).replace(tzinfo=pytz.utc).strftime(currentDateFormat)
            except:
                raise

            name = schedconfigData[schedconfigQueue]["name"]
            queue = schedconfigData[schedconfigQueue]["queue"]
            localqueue = schedconfigData[schedconfigQueue]["localqueue"]
            system = schedconfigData[schedconfigQueue]["system"]
            sysconfig = schedconfigData[schedconfigQueue]["sysconfig"]
            environ = schedconfigData[schedconfigQueue]["environ"]
            gatekeeper = schedconfigData[schedconfigQueue]["gatekeeper"]
            jobmanager = schedconfigData[schedconfigQueue]["jobmanager"]
            se = schedconfigData[schedconfigQueue]["se"]
            ddm = schedconfigData[schedconfigQueue]["ddm"]
            jdladd = schedconfigData[schedconfigQueue]["jdladd"]
            globusadd = schedconfigData[schedconfigQueue]["globusadd"]
            jdl = schedconfigData[schedconfigQueue]["jdl"]
            jdltxt = schedconfigData[schedconfigQueue]["jdltxt"]
            version = schedconfigData[schedconfigQueue]["version"]
            site = schedconfigData[schedconfigQueue]["site"]
            region = schedconfigData[schedconfigQueue]["region"]
            gstat = schedconfigData[schedconfigQueue]["gstat"]
            tags = schedconfigData[schedconfigQueue]["tags"]
            cmd = schedconfigData[schedconfigQueue]["cmd"]
            errinfo = schedconfigData[schedconfigQueue]["errinfo"]
            nqueue = schedconfigData[schedconfigQueue]["nqueue"]
            comment_ = schedconfigData[schedconfigQueue]["comment_"]
            appdir = schedconfigData[schedconfigQueue]["appdir"]
            datadir = schedconfigData[schedconfigQueue]["datadir"]
            tmpdir = schedconfigData[schedconfigQueue]["tmpdir"]
            wntmpdir = schedconfigData[schedconfigQueue]["wntmpdir"]
            dq2url = schedconfigData[schedconfigQueue]["dq2url"]
            special_par = schedconfigData[schedconfigQueue]["special_par"]
            python_path = schedconfigData[schedconfigQueue]["python_path"]
            nodes = schedconfigData[schedconfigQueue]["nodes"]
            status = schedconfigData[schedconfigQueue]["status"]
            copytool = schedconfigData[schedconfigQueue]["copytool"]
            copysetup = schedconfigData[schedconfigQueue]["copysetup"]
            releases = schedconfigData[schedconfigQueue]["releases"]
            sepath = schedconfigData[schedconfigQueue]["sepath"]
            envsetup = schedconfigData[schedconfigQueue]["envsetup"]
            copyprefix = schedconfigData[schedconfigQueue]["copyprefix"]
            lfcpath = schedconfigData[schedconfigQueue]["lfcpath"]
            seopt = schedconfigData[schedconfigQueue]["seopt"]
            sein = schedconfigData[schedconfigQueue]["sein"]
            seinopt = schedconfigData[schedconfigQueue]["seinopt"]
            lfchost = schedconfigData[schedconfigQueue]["lfchost"]
            cloud = schedconfigData[schedconfigQueue]["cloud"]
            siteid = schedconfigData[schedconfigQueue]["siteid"]
            proxy = schedconfigData[schedconfigQueue]["proxy"]
            retry = schedconfigData[schedconfigQueue]["retry"]
            queuehours = schedconfigData[schedconfigQueue]["queuehours"]
            envsetupin = schedconfigData[schedconfigQueue]["envsetupin"]
            copytoolin = schedconfigData[schedconfigQueue]["copytoolin"]
            copysetupin = schedconfigData[schedconfigQueue]["copysetupin"]
            seprodpath = schedconfigData[schedconfigQueue]["seprodpath"]
            lfcprodpath = schedconfigData[schedconfigQueue]["lfcprodpath"]
            copyprefixin = schedconfigData[schedconfigQueue]["copyprefixin"]
            recoverdir = schedconfigData[schedconfigQueue]["recoverdir"]
            memory = schedconfigData[schedconfigQueue]["memory"]
            maxtime = schedconfigData[schedconfigQueue]["maxtime"]
            space = schedconfigData[schedconfigQueue]["space"]
            tspace = schedconfigData[schedconfigQueue]["tspace"]
            if tspace is None:
                tspace = currentDate
            cmtconfig = schedconfigData[schedconfigQueue]["cmtconfig"]
            setokens = schedconfigData[schedconfigQueue]["setokens"]
            glexec = schedconfigData[schedconfigQueue]["glexec"]
            priorityoffset = schedconfigData[schedconfigQueue]["priorityoffset"]
            allowedgroups = schedconfigData[schedconfigQueue]["allowedgroups"]
            defaulttoken = schedconfigData[schedconfigQueue]["defaulttoken"]
            pcache = schedconfigData[schedconfigQueue]["pcache"]
            validatedreleases = schedconfigData[schedconfigQueue]["validatedreleases"]
            accesscontrol = schedconfigData[schedconfigQueue]["accesscontrol"]
            dn = schedconfigData[schedconfigQueue]["dn"]
            email = schedconfigData[schedconfigQueue]["email"]
            allowednode = schedconfigData[schedconfigQueue]["allowednode"]
            maxinputsize = schedconfigData[schedconfigQueue]["maxinputsize"]
            timefloor = schedconfigData[schedconfigQueue]["timefloor"]
            depthboost = schedconfigData[schedconfigQueue]["depthboost"]
            idlepilotsupression = schedconfigData[schedconfigQueue]["idlepilotsupression"]
            pilotlimit = schedconfigData[schedconfigQueue]["pilotlimit"]
            transferringlimit = schedconfigData[schedconfigQueue]["transferringlimit"]
            cachedse = schedconfigData[schedconfigQueue]["cachedse"]
            corecount = schedconfigData[schedconfigQueue]["corecount"]
            countrygroup = schedconfigData[schedconfigQueue]["countrygroup"]
            availablecpu = schedconfigData[schedconfigQueue]["availablecpu"]
            availablestorage = schedconfigData[schedconfigQueue]["availablestorage"]
            pledgedcpu = schedconfigData[schedconfigQueue]["pledgedcpu"]
            pledgedstorage = schedconfigData[schedconfigQueue]["pledgedstorage"]
            statusoverride = schedconfigData[schedconfigQueue]["statusoverride"]
            allowdirectaccess = schedconfigData[schedconfigQueue]["allowdirectaccess"]
            gocname = schedconfigData[schedconfigQueue]["gocname"]
            tier = schedconfigData[schedconfigQueue]["tier"]
            multicloud = schedconfigData[schedconfigQueue]["multicloud"]
            lfcregister = schedconfigData[schedconfigQueue]["lfcregister"]
            stageinretry = schedconfigData[schedconfigQueue]["stageinretry"]
            stageoutretry = schedconfigData[schedconfigQueue]["stageoutretry"]
            fairsharepolicy = schedconfigData[schedconfigQueue]["fairsharepolicy"]
            allowfax = schedconfigData[schedconfigQueue]["allowfax"]
            faxredirector = schedconfigData[schedconfigQueue]["faxredirector"]
            maxwdir = schedconfigData[schedconfigQueue]["maxwdir"]
            try:
                celist = schedconfigData[schedconfigQueue]["celist"]
            except KeyError:
                celist = None
            minmemory = schedconfigData[schedconfigQueue]["minmemory"]
            maxmemory = schedconfigData[schedconfigQueue]["maxmemory"]
            mintime = schedconfigData[schedconfigQueue]["mintime"]

            try:
                _logger.debug('mark')
                oldQueue = Schedconfig.objects.get(nickname=nickname)
                _logger.debug('mark')
                nUpdated = Schedconfig.objects.filter(nickname=nickname).update(\
                name=name, queue=queue, localqueue=localqueue, system=system, \
                sysconfig=sysconfig, environ=environ, gatekeeper=gatekeeper, \
                jobmanager=jobmanager, se=se, ddm=ddm, jdladd=jdladd, \
                globusadd=globusadd, jdl=jdl, jdltxt=jdltxt, version=version, \
                site=site, region=region, gstat=gstat, tags=tags, cmd=cmd, \
                lastmod=lastmod, errinfo=errinfo, nqueue=nqueue, \
                comment_=comment_, appdir=appdir, datadir=datadir, \
                tmpdir=tmpdir, wntmpdir=wntmpdir, dq2url=dq2url, \
                special_par=special_par, python_path=python_path, nodes=nodes, \
                status=status, copytool=copytool, copysetup=copysetup, \
                releases=releases, sepath=sepath, envsetup=envsetup, \
                copyprefix=copyprefix, lfcpath=lfcpath, seopt=seopt, sein=sein, \
                seinopt=seinopt, lfchost=lfchost, cloud=cloud, siteid=siteid, \
                proxy=proxy, retry=retry, queuehours=queuehours, \
                envsetupin=envsetupin, copytoolin=copytoolin, \
                copysetupin=copysetupin, seprodpath=seprodpath, \
                lfcprodpath=lfcprodpath, copyprefixin=copyprefixin, \
                recoverdir=recoverdir, memory=memory, maxtime=maxtime, \
                space=space, tspace=tspace, cmtconfig=cmtconfig, \
                setokens=setokens, glexec=glexec, priorityoffset=priorityoffset, \
                allowedgroups=allowedgroups, defaulttoken=defaulttoken, \
                pcache=pcache, validatedreleases=validatedreleases, \
                accesscontrol=accesscontrol, dn=dn, email=email, \
                allowednode=allowednode, maxinputsize=maxinputsize, \
                timefloor=timefloor, depthboost=depthboost, \
                idlepilotsupression=idlepilotsupression, pilotlimit=pilotlimit, \
                transferringlimit=transferringlimit, cachedse=cachedse, \
                corecount=corecount, countrygroup=countrygroup, \
                availablecpu=availablecpu, availablestorage=availablestorage, \
                pledgedcpu=pledgedcpu, pledgedstorage=pledgedstorage, \
                statusoverride=statusoverride, \
                allowdirectaccess=allowdirectaccess, gocname=gocname, tier=tier, \
                multicloud=multicloud, lfcregister=lfcregister, \
                stageinretry=stageinretry, stageoutretry=stageoutretry, \
                fairsharepolicy=fairsharepolicy, allowfax=allowfax, \
                faxredirector=faxredirector, maxwdir=maxwdir, celist=celist, \
                minmemory=minmemory, maxmemory=maxmemory, mintime=mintime \
                )
                newQueue = Schedconfig.objects.get(nickname=nickname)
                diff = {}
                for field in newQueue.__dict__:
                    if oldQueue.__dict__[field] != newQueue.__dict__[field] \
                    and field != '_state':
                        diff[field] = {'old': str(oldQueue.__dict__[field]), \
                                       'new': str(newQueue.__dict__[field])}
                _logger.debug('type(newQueue)=%s data=%s' % (type(newQueue), newQueue))
                _logger.debug('type(nUpdated)=%s data=%s' % (type(nUpdated), nUpdated))
#                result += getResultString(schedconfigQueue, diff, action='Updated')
                result.append({
                               'action': 'Updated',
                               'nickname': schedconfigQueue,
                               'diff': diff
                               })

            except ObjectDoesNotExist:
                _logger.debug('mark')
                newQueue = Schedconfig.objects.get_or_create(nickname=nickname, \
                name=name, queue=queue, localqueue=localqueue, system=system, \
                sysconfig=sysconfig, environ=environ, gatekeeper=gatekeeper, \
                jobmanager=jobmanager, se=se, ddm=ddm, jdladd=jdladd, \
                globusadd=globusadd, jdl=jdl, jdltxt=jdltxt, version=version, \
                site=site, region=region, gstat=gstat, tags=tags, cmd=cmd, \
                lastmod=lastmod, errinfo=errinfo, nqueue=nqueue, \
                comment_=comment_, appdir=appdir, datadir=datadir, \
                tmpdir=tmpdir, wntmpdir=wntmpdir, dq2url=dq2url, \
                special_par=special_par, python_path=python_path, nodes=nodes, \
                status=status, copytool=copytool, copysetup=copysetup, \
                releases=releases, sepath=sepath, envsetup=envsetup, \
                copyprefix=copyprefix, lfcpath=lfcpath, seopt=seopt, sein=sein, \
                seinopt=seinopt, lfchost=lfchost, cloud=cloud, siteid=siteid, \
                proxy=proxy, retry=retry, queuehours=queuehours, \
                envsetupin=envsetupin, copytoolin=copytoolin, \
                copysetupin=copysetupin, seprodpath=seprodpath, \
                lfcprodpath=lfcprodpath, copyprefixin=copyprefixin, \
                recoverdir=recoverdir, memory=memory, maxtime=maxtime, \
                space=space, tspace=tspace, cmtconfig=cmtconfig, \
                setokens=setokens, glexec=glexec, priorityoffset=priorityoffset, \
                allowedgroups=allowedgroups, defaulttoken=defaulttoken, \
                pcache=pcache, validatedreleases=validatedreleases, \
                accesscontrol=accesscontrol, dn=dn, email=email, \
                allowednode=allowednode, maxinputsize=maxinputsize, \
                timefloor=timefloor, depthboost=depthboost, \
                idlepilotsupression=idlepilotsupression, pilotlimit=pilotlimit, \
                transferringlimit=transferringlimit, cachedse=cachedse, \
                corecount=corecount, countrygroup=countrygroup, \
                availablecpu=availablecpu, availablestorage=availablestorage, \
                pledgedcpu=pledgedcpu, pledgedstorage=pledgedstorage, \
                statusoverride=statusoverride, \
                allowdirectaccess=allowdirectaccess, gocname=gocname, tier=tier, \
                multicloud=multicloud, lfcregister=lfcregister, \
                stageinretry=stageinretry, stageoutretry=stageoutretry, \
                fairsharepolicy=fairsharepolicy, allowfax=allowfax, \
                faxredirector=faxredirector, maxwdir=maxwdir, celist=celist, \
                minmemory=minmemory, maxmemory=maxmemory, mintime=mintime \
                )
                _logger.debug('mark')
#                result += "Added schedconfig info for queue " + str(schedconfigQueue) + ".\n"
                result.append({'action': 'Added',
                               'nickname': schedconfigQueue,
                               'diff': {}
                               })
    else:
        result + "Length of output is zero: " + str(SOURCE_SCHEDCONFIG[vo]) + "\n"

    data = {
        'prefix': getPrefix(request),
        'result': result, 'schedconfigQueues': schedconfigQueues,
    }
    data.update(getContextVariables(request))
    return render_to_response('topology/updateSchedconfig.html', data, RequestContext(request))


def listSchedconfigQueues(request):
    jobList = []
    jobList.extend(Schedconfig.objects.order_by('nickname'))
    _logger.debug('schedconfig queue list=' + str(jobList))
    jobList = sorted(jobList, key=lambda x:x.nickname)
    _logger.debug('schedconfig queue list=' + str(jobList))
    data = {
        'prefix': getPrefix(request),
        'jobList': jobList,
    }
    data.update(getContextVariables(request))
    return render_to_response('topology/listSchedconfigQueues.html', data, RequestContext(request))


def schedconfigDetails(request, nickname):
    _logger.debug('nickname = ...%s...' % (nickname))
    schedconfig = {}
    schedconfigList = []
    schedconfigList.append(Schedconfig.objects.filter(nickname=nickname).values())
    if len(schedconfigList):
        try:
            schedconfig = schedconfigList[0][0]
        except IndexError:
            schedconfig = {}
    _logger.debug('type(schedconfig)=%s data=%s' % (type(schedconfig), schedconfig))
    jobInfo = []
    jobKeys = schedconfig.keys()

    for key in sorted(jobKeys):
        jobInfo.append((key, str(schedconfig[key])))
    _logger.debug('schedconfig queue details: ' + str(jobInfo))
    name = nickname
    data = {
        'prefix': getPrefix(request),
        'schedconfigInfo': jobInfo, 'name': name
    }
    data.update(getContextVariables(request))
    return render_to_response('topology/schedconfigDetails.html', data, RequestContext(request))


