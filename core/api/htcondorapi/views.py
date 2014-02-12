""" 
htcondorapi.views

"""
import sys
import json
import logging
import commands
import itertools
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework.views import APIView
from ...htcondor.models import HTCondorJob
from .serializers import SerializerHTCondorJob
from .utils import isSecure, getDN, getFQAN, getRemoteHost, checkBanUser
import status as htcondorapi_status

#_logger = logging.getLogger(__name__)
_logger = logging.getLogger('bigpandamon')

currentDateFormat = "%Y-%m-%d %H:%M:%SZ"

# Create your views here.
class HTCondorJobsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows HTCondor jobs listed
    """
    model = HTCondorJob
    serializer_class = SerializerHTCondorJob


    def initialSecurityChecks(self, request):
        """
            addHTCondorJobs
            args:
                request
            returns:
                status, description
        
        """
        isSecured = False
        # check it is secure request
        if isSecure(request):
            isSecured = True
        # get DN
        user = None
        if request.META.has_key('SSL_CLIENT_S_DN'):
            user = getDN(request)
        # get FQAN
        fqans = getFQAN(request)
        # hostname
        host = getRemoteHost(request)
        # return findings
        return (isSecured, user, fqans, host)


    def addHTCondorJobsOrig(self, request):
        """
            addHTCondorJobs
            args:
                request
            returns:
                Response with HTTP status code
                    data/errors
        
        """
        ### initial security checks
        isSecured, user, fqans, host = self.initialSecurityChecks(request)
        ### if not secured, exit
        if not isSecured:
            return Response({'error': \
                        'Please use https and do not use limited proxy!'}, \
                        status=status.HTTP_401_UNAUTHORIZED)
        ### check user ban status
        if checkBanUser(dn=user, sourceLabel='htcondor'):
            return Response({'error': \
                        'User not allowed to perform this request!'}, \
                        status=status.HTTP_403_FORBIDDEN)
        ### proceed to save
        serializer = SerializerHTCondorJob(data=request.DATA, many=True)
#        _l
        _logger.debug('|serializer.data|=', str(len(serializer.data)))
        _logger.debug('serializer.data=', str(serializer.data))
        if serializer.is_valid():
            ### all fields are filled
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except :
                type, value, traceBack = sys.exc_info()
                _logger.error("addHTCondorJobs : %s %s" % (type, value))
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            ### some fields are not filled or are filled in wrong
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def addHTCondorJobsAction(self, data, user):
        """
        addHTCondorJobsAction
            args:
                data ... data for a single instance of HTCondorJob
                user ... user performing the action
            returns:
                status, description
        """
        ret = htcondorapi_status.HTCAPI_OK
        desc = "OK"
        globaljobid = None
        wmsid = None
        ### Make sure fields are not missing: globaljobid, wmsid
        try:
            globaljobid = data['globaljobid']
        except KeyError:
            ret = htcondorapi_status.HTCAPI_MISSING_FIELD
            desc = "Missing field '%s' in the request data!" % ('globaljobid')
            return (ret, desc)
        try:
            wmsid = data['wmsid']
        except KeyError:
            ret = htcondorapi_status.HTCAPI_MISSING_FIELD
            desc = "Missing field '%s' in the request data!" % ('wmsid')
            return (ret, desc)
        errors = []
        ### Create new HTCondorJob
        try:
            m = HTCondorJob(**data)
            m.save(force_insert=True)
        except:
            ret = htcondorapi_status.HTCAPI_CANNOT_SAVE
            desc = "Cannot add HTCondorJob %s %s" % (globaljobid, wmsid)
            errors.append({'ret': ret, 'desc': desc})
        ### Retrieve existing instances from DB
        htcondorjobs = HTCondorJob.objects.filter(globaljobid=globaljobid, wmsid=wmsid)
        ### Deal with errors
        if errors:
            rret = errors[0]['ret']
            ddesc = errors[0]['desc']
            return (rret, ddesc)
        ### Return
        return (ret, desc)


    def addHTCondorJobs(self, request):
        """
            addHTCondorJobs
            args:
                request
            returns:
                Response with HTTP status code
                    data/errors
            
        """
        ### initial security checks
        isSecured, user, fqans, host = self.initialSecurityChecks(request)
        ### if not secured, exit
        if not isSecured:
            return Response({'error': \
                        'Please use https and do not use limited proxy!'}, \
                        status=status.HTTP_401_UNAUTHORIZED)
        ### check user ban status
        _logger.info('about to do checkBanUser(dn=%s, sourceLabel=\'htcondor\')' % (user))
        if checkBanUser(dn=user, sourceLabel='htcondor'):
            return Response({'error': \
                        'User not allowed to perform this request!'}, \
                        status=status.HTTP_403_FORBIDDEN)
        _logger.info('User passed, is not banned: checkBanUser(dn=%s, sourceLabel=\'htcondor\')' % (user))
        ### proceed to execute action
        errors = []
        for item in request.DATA:
            _logger.debug('item=' + str(item))
            ret, desc = self.addHTCondorJobsAction(item, user)
            if ret != htcondorapi_status.HTCAPI_OK:
                errors.append({'ret': ret, 'desc': desc})
            _logger.debug('ret=' + str(ret))

        if errors:
            return Response(str(list(set([x['desc'] for x in errors]))), status=status.HTTP_400_BAD_REQUEST)

        return Response(request.DATA, status=status.HTTP_201_CREATED)



    def updateHTCondorJobsAction(self, data, user):
        """
        updateHTCondorJobsAction
            args:
                data ... data for a single instance of HTCondorJob
                user ... user performing the action
            returns:
                status, description
        """
        ret = htcondorapi_status.HTCAPI_OK
        desc = "OK"
        globaljobid = None
        wmsid = None
        ### Make sure fields are not missing: globaljobid, wmsid
        try:
            globaljobid = data['globaljobid']
        except KeyError:
            ret = htcondorapi_status.HTCAPI_MISSING_FIELD
            desc = "Missing field '%s' in the request data!" % ('globaljobid')
            return (ret, desc)
        try:
            wmsid = data['wmsid']
        except KeyError:
            ret = htcondorapi_status.HTCAPI_MISSING_FIELD
            desc = "Missing field '%s' in the request data!" % ('wmsid')
            return (ret, desc)
        ### Retrieve existing instances from DB
        htcondorjobs = HTCondorJob.objects.filter(globaljobid=globaljobid, wmsid=wmsid)
        ### Apply changes, n.b. ['globaljobid', 'wmsid'] cannot change!
        dataOptional = {}
        dataOptional.update(data)
        for field in ['globaljobid', 'wmsid']:
            try:
                del dataOptional[field]
            except:
                pass
        errors = []
        ### Update queryset
        try:
            htcondorjobs.update(**dataOptional)
        except:
            ret = htcondorapi_status.HTCAPI_CANNOT_UPDATE
            desc = "Cannot update HTCondorJob %s" % (globaljobid)
            errors.append({'ret': ret, 'desc': desc})
        ### Save changes
        if not errors:
            for htcondorjob in htcondorjobs:
                try:
                    htcondorjob.save()
                except:
                    ret = htcondorapi_status.HTCAPI_CANNOT_SAVE
                    desc = "Cannot save HTCondorJob %s !" % (globaljobid)
                    errors.append({'ret': ret, 'desc': desc})
        ### Deal with errors
        if errors:
            rret = errors[0]['ret']
            ddesc = errors[0]['desc']
            return (rret, ddesc)
        ### Return
        return (ret, desc)


    def updateHTCondorJobs(self, request):
        """
            updateHTCondorJobs
            args:
                request
            returns:
                Response with HTTP status code
                    data/errors
            
        """
        ### initial security checks
        isSecured, user, fqans, host = self.initialSecurityChecks(request)
        ### if not secured, exit
        if not isSecured:
            return Response({'error': \
                        'Please use https and do not use limited proxy!'}, \
                        status=status.HTTP_401_UNAUTHORIZED)
        ### check user ban status
        if checkBanUser(dn=user, sourceLabel='htcondor'):
            return Response({'error': \
                        'User not allowed to perform this request!'}, \
                        status=status.HTTP_403_FORBIDDEN)
        ### proceed to execute action
        errors = []
        for item in request.DATA:
            ret, desc = self.updateHTCondorJobsAction(item, user)
            if ret != htcondorapi_status.HTCAPI_OK:
                errors.append({'ret': ret, 'desc': desc})

        if errors:
            return Response(str(list(set([x['desc'] for x in errors]))), status=status.HTTP_400_BAD_REQUEST)

        return Response(request.DATA, status=status.HTTP_202_ACCEPTED)


    def removeHTCondorJobsAction(self, data, user):
        """
        removeHTCondorJobsAction
            args:
                data ... data for a single instance of HTCondorJob
                user ... user performing the action
            returns:
                status, description
        """
        ret=htcondorapi_status.HTCAPI_OK
        desc="OK"
        globaljobid = None
        ### Check that compulsory field is available
        try:
            globaljobid = data['globaljobid']
        except KeyError:
            ret = htcondorapi_status.HTCAPI_MISSING_FIELD
            desc = "Missing field '%s' in the request data!" % ('globaljobid')
            return (ret, desc)
        ### Retrieve existing instances from DB
        htcondorjobs = HTCondorJob.objects.filter(globaljobid=globaljobid)
        errors = []
        ### Update instances and save
        for htcondorjob in htcondorjobs:
            htcondorjob.removed = True
#            #TODO: #FIXME add fields removedbyuser and removedtime to the schema
#            htcondorjob.removedbyuser = user
#            htcondorjob.removedtime = "%s" % (commands.getoutput("date '+%F %H:%M:%S' -u"))
            try:
                htcondorjob.save()
            except:
                ret = htcondorapi_status.HTCAPI_CANNOT_SAVE
                desc = "Cannot save HTCondorJob %s" % (globaljobid)
                errors.append({'ret': ret, 'desc': desc})
        ### Deal with errors
        if errors:
            rret = errors[0]['ret']
            ddesc = errors[0]['desc']
            return (rret, ddesc)
        ### Return
        return (ret, desc)


    def removeHTCondorJobs(self, request):
        """
            removeHTCondorJobs
            args:
                request
            returns:
                Response with HTTP status code
                    data/errors
        
        """
        ### initial security checks
        isSecured, user, fqans, host = self.initialSecurityChecks(request)
        ### if not secured, exit
        if not isSecured:
            return Response({'error': \
                        'Please use https and do not use limited proxy!'}, \
                        status=status.HTTP_401_UNAUTHORIZED)
        ### check user ban status
        if checkBanUser(dn=user, sourceLabel='htcondor'):
            return Response({'error': \
                        'User not allowed to perform this request!'}, \
                        status=status.HTTP_403_FORBIDDEN)
        ### proceed to execute action
        errors = []
        for item in request.DATA:
            ret, desc = self.removeHTCondorJobsAction(item, user)
            if ret != htcondorapi_status.HTCAPI_OK:
                errors.append({'ret': ret, 'desc': desc})

        if errors:
            return Response(str(list(set([x['desc'] for x in errors]))), status=status.HTTP_400_BAD_REQUEST)

        return Response(request.DATA, status=status.HTTP_202_ACCEPTED)


    def list(self, request):
        """
            list
            args:
                request
            returns:
                Response with HTTP status code
                    data/errors
        
        """
        queryset = list(itertools.chain(HTCondorJob.objects.all()))
        serializer = SerializerHTCondorJob(queryset, many=True)
        return Response(serializer.data)


    def listForDataTables(self, request):
        """
            listForDataTables
            args:
                request
            returns:
                Response with HTTP status code
                    data/errors
        
        """
        queryset = list(itertools.chain(HTCondorJob.objects.all()))
        serializer = SerializerHTCondorJob(queryset, many=True)
        data = serializer.data[:5]
#        data = serializer.data
        return Response({"aaData": data, "result": "ok", \
#                         "sEcho": 0, \
                         "iTotalRecords": len(data), \
                         "iTotalDisplayRecords": len(data) \
                    })


