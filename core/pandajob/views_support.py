import logging

from django.shortcuts import render_to_response
from django.template import RequestContext

from core.pandajob.models import Jobsarchived4

_logger = logging.getLogger('bigpandamon')

def maxpandaid(request):
    """
        Support view to return maxpandaid in the jobsarchived4 table.
        Helps to collect LSST logs when "xrdfs ls" times out.
    """
    try:
        pandaid = Jobsarchived4.objects.all().order_by("-pandaid").values()[0]['pandaid']
    except:
        pandaid = 0
    return render_to_response('pandajob/support/maxpandaid.html', {'maxpandaid': pandaid}, RequestContext(request))


