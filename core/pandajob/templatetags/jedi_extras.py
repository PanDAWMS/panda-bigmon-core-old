"""
jedi_extras -- template tags for JEDImon in core.pandajob

"""

import logging
from django import template
from django.template.loader import render_to_string
#from core.common.utils import getPrefix, getContextVariables
from ...common.utils import getPrefix, getContextVariables, getAoColumnsList

_logger = logging.getLogger('jedi_extra')


register = template.Library()


#@register.simple_tag
#def empty_div(*args, **kwargs):
#    return render_to_string('templatetags/empty_div.html', {})


@register.simple_tag
def jedi_jobs_table_with_filter(\
        datasrc, datasrcsmry, data, columns, tableid, tableidsmry, \
        caption="", filterFields={}, fieldIndices={}, \
        template='templatetags/jedi/jedi_jobs_table_with_filter.html', \
            *args, **kwargs):
    """
#        template tag with the javascript functionality 
        for the job list table and corresponding filter table
        
    """
#    template = 'templatetags/jedi/jedi_jobs_table_with_filter.html'
    returnData = { \
             'tableid': tableid, \
             'tableidsmry': tableidsmry, \
             'caption': caption, \
             'datasrc': datasrc, \
             'datasrcsmry': datasrcsmry, \
             'data': data, \
             'columns': columns, \
             'filterFields': filterFields, \
             'fieldIndices': fieldIndices, \
             }
    _logger.debug('returnData=' + str(returnData))
    returnData.update(getContextVariables(None))
    return render_to_string(template, returnData)


@register.simple_tag
def jedi_table_jobs(datasrc, data, columns, tableid, \
        caption="", filterFields={}, fieldIndices={}, \
        template='templatetags/jedi/jedi_table_jobs.html', \
            *args, **kwargs):
    """
        template tag with the HTML table for the job list
        
    """
#    template = 'templatetags/jedi/jedi_table_jobs.html'
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
def jedi_smry_jobs(datasrcsmry, data, columns, tableidsmry, \
        caption="", filterFields={}, fieldIndices={}, \
        template='templatetags/jedi/jedi_smry_jobs.html', \
            *args, **kwargs):
    """
        template tag with the HTML table for the job list summary
        
    """
#    template = 'templatetags/jedi/jedi_smry_jobs.html'
    returnData = { \
             'tableidsmry': tableidsmry, \
             'caption': caption, \
             'datasrcsmry': datasrcsmry, \
             'data': data, \
             'columns': columns, \
             'filterFields': filterFields, \
             'fieldIndices': fieldIndices, \
             }
    _logger.debug('returnData=' + str(returnData))
    returnData.update(getContextVariables(None))
    return render_to_string(template, returnData)


@register.simple_tag
def jedi_table_filter(datasrc, data, columns, tableid, \
        caption="", filterFields={}, fieldIndices={}, \
        template='templatetags/jedi/jedi_table_filter.html', \
            *args, **kwargs):
    """
        template tag with the HTML table for the filter
        
    """
#    template = 'templatetags/jedi/jedi_table_filter.html'
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


