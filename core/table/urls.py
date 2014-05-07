from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
### #FIXME admin.autodiscover()

#from core import views as core_views
#from topology import views as topology_views
#from htcondor import views as htcondor_views
#from api.htcondorapi import views as htcondorapi_views
from ..pandajob import views as pandajob_views
from ..htcondor import views as htcondor_views

urlpatterns = patterns('',
    ### dataTables food
    url(r'^/htcondorjob/$', htcondor_views.HTCondorJobDictJson.as_view(), name='api-datatables-htcondor-jobs'),
    url(r'^/pandajob/$', pandajob_views.PandaJobDictJson.as_view(), name='api-datatables-panda-jobs'),
)


