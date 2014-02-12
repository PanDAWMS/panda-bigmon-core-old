"""
htcondorapi.utils -- utilities for secured API

"""
import logging
import re
from ...core.models import Users

#_logger = logging.getLogger(__name__)
_logger = logging.getLogger('bigpandamon')


# security check
# check if secure connection
def isSecure(req):
    # check security
    if not req.META.has_key('SSL_CLIENT_S_DN'):
        return False
    # disable limited proxy
    if '/CN=limited proxy' in req.META['SSL_CLIENT_S_DN']:
        _logger.warning("access via limited proxy : %s" % req.subprocess_env['SSL_CLIENT_S_DN'])
        return False
    return True


# get FQANs
def getFQAN(req):
    fqans = []
    for tmpKey, tmpVal in req.META.iteritems():
        # compact credentials
        if tmpKey.startswith('GRST_CRED_'):
            # VOMS attribute
            if tmpVal.startswith('VOMS'):
                # FQAN
                fqan = tmpVal.split()[-1]
                # append
                fqans.append(fqan)
        # old style
        elif tmpKey.startswith('GRST_CONN_'):
            tmpItems = tmpVal.split(':')
            # FQAN
            if len(tmpItems) == 2 and tmpItems[0] == 'fqan':
                fqans.append(tmpItems[-1])
    return fqans


# get DN
def getDN(req):
    realDN = ''
    if req.META.has_key('SSL_CLIENT_S_DN'):
        realDN = req.META['SSL_CLIENT_S_DN']
        # remove redundant CN
        realDN = re.sub('/CN=limited proxy', '', realDN)
        realDN = re.sub('/CN=proxy(/CN=proxy)+', '/CN=proxy', realDN)
    return realDN


# get remote host
def getRemoteHost(req):
    host = ''
    if req.META.has_key('REMOTE_HOST'):
        host = req.META['REMOTE_HOST']
    return host


# extract name from DN
def cleanUserID(id):
    """
    cleanUserID : get username from DN
    
    """
    try:
        up = re.compile('/(DC|O|OU|C|L)=[^\/]+')
        username = up.sub('', id)
        up2 = re.compile('/CN=[0-9]+')
        username = up2.sub('', username)
        up3 = re.compile(' [0-9]+')
        username = up3.sub('', username)
        up4 = re.compile('_[0-9]+')
        username = up4.sub('', username)
        username = username.replace('/CN=proxy', '')
        username = username.replace('/CN=limited proxy', '')
        username = username.replace('limited proxy', '')
        username = re.sub('/CN=Robot:[^/]+', '', username)
        pat = re.compile('.*/CN=([^\/]+)/CN=([^\/]+)')
        mat = pat.match(username)
        if mat:
            username = mat.group(2)
        else:
            username = username.replace('/CN=', '')
        if username.lower().find('/email') > 0:
            username = username[:username.lower().find('/email')]
        pat = re.compile('.*(limited.*proxy).*')
        mat = pat.match(username)
        if mat:
            username = mat.group(1)
        username = username.replace('(', '')
        username = username.replace(')', '')
        username = username.replace("'", '')
        return username
    except:
        return id


# check banned user
def checkBanUser(dn, sourceLabel=None):
    """
        checkBanUser : check if user is banned in PanDA
        args:
            dn : certificate DN from request field SSL_CLIENT_S_DN
            sourceLabel : optional
        response:
            True : user is banned
            False : user is not banned
            default: user is not banned
        
    """
    ### get clean name from DN
    name = cleanUserID(dn)
    _logger.debug('checkBanUser: dn=%s' % (dn))
    _logger.debug('checkBanUser: name=%s' % (name))
    ### list all users with this name
    users = Users.objects.filter(name=name)
    ret = False
    if sourceLabel == 'htcondor':
        if not len(users):
            ret = True
    ### get status of the user
    if len(users):
        for user in users:
            if user.status in ["disabled"]:
                ret = True
    return ret


