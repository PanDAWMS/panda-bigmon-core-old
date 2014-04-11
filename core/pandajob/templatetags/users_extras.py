"""
users_extras -- template tags for User activity in core.pandajob

"""

import logging
from django import template
from django.template.loader import render_to_string
#from core.common.utils import getPrefix, getContextVariables
from ...common.utils import getPrefix, getContextVariables, getAoColumnsList

_logger = logging.getLogger('users_extra')


register = template.Library()


@register.simple_tag
def users_list_active(datasrc, data, columns, tableid, \
        caption="", filterFields={}, fieldIndices={}, \
        template='templatetags/users/users_list_active.html', \
            *args, **kwargs):
    """
        template tag with the HTML table for the job list
        
    """
    returnData = { \
             'tableid': tableid, \
             'caption': caption, \
             'datasrc': datasrc, \
             'data': data, \
             'columns': columns, \
             'filterFields': filterFields, \
             'fieldIndices': fieldIndices, \
             }
    _logger.debug('returnData=' + str(returnData))
    returnData.update(getContextVariables(None))
    return render_to_string(template, returnData)


