""" 
utils

"""
import logging
from itertools import islice, chain
#from ..settings import STATIC_URL, ENV
#from settings import STATIC_URL, FILTER_UI_ENV
#from django.conf.settings import STATIC_URL, FILTER_UI_ENV
from django.conf import settings
#.settings import STATIC_URL, FILTER_UI_ENV


try:
    from settings import URL_PATH_PREFIX
except ImportError:
    URL_PATH_PREFIX = None

#_logger = logging.getLogger(__name__)
_logger = logging.getLogger('bigpandamon')


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
    ret = { 'STATIC_URL': settings.STATIC_URL, 'prefix': getPrefix(request) }
    try:
        ret.update(ENV)
    except:
        ret = ret
    return ret


def getAoColumnsList(columnList):
    return [ {"sTitle": "%s" % (column)} for column in columnList ]

def getAoColumnsDict(columnList):
    return [ {"sTitle": "%s" % (column), "mDataProp": "%s" % (column) } for column in columnList ]

def getAoColumnsDictWithTitles(columnDescriptionList):
    data = []
    for item in columnDescriptionList:
        _logger.debug('item=' + str(item))
        try:
            fvis = item['vis']
        except KeyError:
            fvis = "false"
        fsort = fvis
        data.append({\
                "sTitle": item['t'], \
                "mDataProp": item['c'], \
                "bSearchable": True, \
                "bSortable": fsort, \
                "bVisible": fvis, \
            })
    return data


class QuerySetChain(object):
    """
    Chains multiple subquerysets (possibly of different models) and behaves as
    one queryset.  Supports minimal methods needed for use with
    django.core.paginator.
    """

    def __init__(self, *subquerysets):
        self.querysets = subquerysets
        self.query = None

    def count(self):
        """
        Performs a .count() for all subquerysets and returns the number of
        records as an integer.
        """
        return sum(qs.count() for qs in self.querysets)

    def _clone(self):
        "Returns a clone of this queryset chain"
        return self.__class__(*self.querysets)

    def _all(self):
        "Iterates records in all subquerysets"
        return chain(*self.querysets)

    def __getitem__(self, ndx):
        """
        Retrieves an item or slice from the chained set of results from all
        subquerysets.
        """
        if type(ndx) is slice:
            return list(islice(self._all(), ndx.start, ndx.stop, ndx.step or 1))
        else:
            return islice(self._all(), ndx, ndx + 1).next()

    def order_by(self, *field_names):
        """
        Returns a new QuerySetChain instance with the ordering changed.
        """
        ret = []
        for qs in self.querysets:
            ret.extend(qs)
        for field in field_names:
            if field[0] == '-':
                ### lambda x:-x[field[1:]] is failing with TypeError
                ### for -datetime.datetime,
                ###     --> use reverse instead
                ret = sorted(ret, key=lambda x:x[field[1:]], reverse=True)
            else:
                ret = sorted(ret, key=lambda x:x[field], reverse=False)
        return ret

    @property
    def len(self):
        """
            get length of QueryChain list
        """
        return self.count()


def subDict(somedict, somekeys, default=None):
    """
        Returns subset of a dictionary with keys from somekeys
    
    """
    return dict([ (k, somedict.get(k, default)) for k in somekeys ])


def subDictToStr(somedict, somekeys, datetimeKeys, desiredDateFormat, default=None):
    """
        Returns subset of a dictionary with keys from somekeys. 
    
    """
    retDict = dict([ (k, somedict.get(k, default)) for k in somekeys ])
    for datetimeKey in datetimeKeys:
        try:
            value = retDict[datetimeKey]
        except:
            _logger.error('Something went wrong, expected field %s not found' % datetimeKey)
        try:
            value = value.strftime(desiredDateFormat)
        except:
            _logger.error('Something went wrong, date %s type %s format %s ' % (value, type(value), desiredDateFormat))
        try:
            retDict[datetimeKey] = value
        except:
            _logger.error('Something went wrong, could not set new value [] for key []' % (value, datetimeKey))
    return retDict


