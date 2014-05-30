import logging, re
from datetime import datetime, timedelta

from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.template import RequestContext, loader
from django.db.models import Count
from django import forms
from django.views.decorators.csrf import csrf_exempt

from core.common.utils import getPrefix, getContextVariables, QuerySetChain
from core.common.settings import STATIC_URL, FILTER_UI_ENV, defaultDatetimeFormat
from core.pandajob.models import PandaJob, Jobsactive4, Jobsdefined4, Jobswaiting4, Jobsarchived4, Jobsarchived
from core.resource.models import Schedconfig
from core.common.models import Filestable4 
from core.common.models import FilestableArch
from core.common.models import Users
from core.common.models import Jobparamstable
from core.common.models import Logstable
from core.common.models import JediJobRetryHistory
from core.common.models import JediTasks
from core.common.settings.config import ENV

from settings.local import dbaccess

_logger = logging.getLogger('bigpandamon')

def maxpandaid(request):
    """
        Support view to return maxpandaid in the jobsarchived4 table.
        Helps to collect LSST logs when "xrdfs ls" times out.
    """
    try:
        pandaid = Jobsarchived4.objects.all().order_by("-pandaid")[0]
    except:
        pandaid = 0
    return render_to_response('maxpandaid.html', {'maxpandaid': pandaid}, RequestContext(request))


