"""
core_extras -- template tags for core

"""

from django import template
from django.template.loader import render_to_string
from ..utils import getPrefix, getContextVariables

register = template.Library()


@register.simple_tag
def top_menu_item(caption, url, target='_blank', *args, **kwargs):
    return render_to_string('templatetags/top_menu_item.html', \
            {'caption': caption, 'url': url, 'target': target , \
             'prefix': getPrefix(None)})


@register.simple_tag
def empty_div(*args, **kwargs):
    return render_to_string('templatetags/empty_div.html', {})


@register.simple_tag
def joblist(datasrc, data, columns, tableid, caption="", showdatasrc=0, \
            listType="HTCondor", model="HTCondor", *args, **kwargs):
    template = 'templatetags/joblist_dict.html'
    returnData = { \
             'tableid': tableid, \
             'caption': caption, \
             'showdatasrc': showdatasrc, \
             'datasrc': datasrc, \
             'data': data, \
             'columns': columns, \
             'model': model, \
             }
    returnData.update(getContextVariables(None))
    return render_to_string(template, returnData)

