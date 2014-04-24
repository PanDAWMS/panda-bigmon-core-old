""" 
utils

"""

from ..settings import STATIC_URL, ENV
try:
    from ..settings import URL_PATH_PREFIX
except ImportError:
    URL_PATH_PREFIX = None

def getPrefix(request):
    """
    getPrefix of multi-user URL
    /bigpandamon/ --> '/bigpandamon'
    
    """
    if URL_PATH_PREFIX is not None:
        return URL_PATH_PREFIX
    else:
        res = '/'
        try:
            res = '/' + str(request.path).split('/')[1]
        except IndexError:
            res = '/'
        return res


def getContextVariables(request):
    """
    getContextVariables: build dictionary for context
    
    """
    ret = { 'STATIC_URL': STATIC_URL, 'prefix': getPrefix(request) }
    try:
        ret.update(ENV)
    except:
        ret = ret
    return ret


