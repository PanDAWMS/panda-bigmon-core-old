"""
users_extras -- template tags for User activity in core.pandajob

"""

import logging
from django import template
from django.template.loader import render_to_string
#from core.common.utils import getPrefix, getContextVariables
from ...common.utils import getPrefix, getContextVariables, getAoColumnsList
from .jedi_extras import jedi_jobs_table_with_filter, jedi_table_jobs, \
    jedi_smry_jobs, jedi_table_filter


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


@register.simple_tag
def users_jobs_table_with_filter(\
        datasrc, datasrcsmry, data, columns, tableid, tableidsmry, \
        caption="", filterFields={}, fieldIndices={}, \
        template='templatetags/users/users_jobs_table_with_filter.html', \
            *args, **kwargs):
    return jedi_jobs_table_with_filter(\
        datasrc, datasrcsmry, data, columns, tableid, tableidsmry, \
        caption=caption, filterFields=filterFields, fieldIndices=fieldIndices, \
        template=template, *args, **kwargs)
    """
        template tag with the javascript functionality 
        for the job list table and corresponding filter table
        
    """


@register.simple_tag
def users_table_jobs(datasrc, data, columns, tableid, \
        caption="", filterFields={}, fieldIndices={}, \
        template='templatetags/users/users_table_jobs.html', \
            *args, **kwargs):
    return jedi_table_jobs(datasrc, data, columns, tableid, \
        caption=caption, filterFields=filterFields, fieldIndices=fieldIndices, \
        template=template, *args, **kwargs)
    """
        template tag with the HTML table for the job list
        
    """


@register.simple_tag
def users_smry_jobs(datasrcsmry, data, columns, tableidsmry, \
        caption="", filterFields={}, fieldIndices={}, \
        template='templatetags/users/users_smry_jobs.html', \
            *args, **kwargs):
    return jedi_smry_jobs(datasrcsmry, data, columns, tableidsmry, \
        caption=caption, filterFields=filterFields, fieldIndices=fieldIndices, \
        template=template, *args, **kwargs)
    """
        template tag with the HTML table for the job list summary
        
    """


@register.simple_tag
def users_table_filter(datasrc, data, columns, tableid, \
        caption="", filterFields={}, fieldIndices={}, \
        template='templatetags/users/users_table_filter.html', \
            *args, **kwargs):
    return jedi_table_filter(datasrc, data, columns, tableid, \
        caption=caption, filterFields=filterFields, fieldIndices=fieldIndices, \
        template=template, *args, **kwargs)
    """
        template tag with the HTML table for the filter
        
    """
