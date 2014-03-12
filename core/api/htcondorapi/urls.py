from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
### #FIXME admin.autodiscover()

#from core import views as core_views
#from topology import views as topology_views
#from htcondor import views as htcondor_views
import views as htcondorapi_views

#### Actions of HTCondor API
#htcondorapi_addjob = htcondorapi_views.HTCondorJobsViewSet.as_view(
#{
#    'get': 'list',
#    'post': 'addHTCondorJobs',
#})
#htcondorapi_updatejob = htcondorapi_views.HTCondorJobsViewSet.as_view(
#{
#    'get': 'list',
#    'post': 'updateHTCondorJobs',
#})
#htcondorapi_removejob = htcondorapi_views.HTCondorJobsViewSet.as_view(
#{
#    'get': 'list',
#    'post': 'removeHTCondorJobs',
#})
#htcondorapi_listjob = htcondorapi_views.HTCondorJobsViewSet.as_view(
#{
#    'get': 'listForDataTables',
#})
htcondorapi_jobs_bulk = htcondorapi_views.HTCondorJobsViewSet.as_view(
{
    'post': 'addHTCondorJobs',
    'get': 'list',
    'put': 'updateHTCondorJobs',
    'delete': 'removeHTCondorJobs',
})

urlpatterns = patterns('',
    ### REST framework API
#    url(r'^api-auth/htcondorapi/addjob/$', htcondorapi_addjob, name='htcondorapi-add-job'),
#    url(r'^api-auth/htcondorapi/updatejob/$', htcondorapi_updatejob, name='htcondorapi-update-job'),
#    url(r'^api-auth/htcondorapi/removejob/$', htcondorapi_removejob, name='htcondorapi-remove-job'),
#    url(r'^api/listall/htcondor/$', htcondorapi_listjob, name='api-datatables-htcondor-dict'),
    url(r'^jobs/$', htcondorapi_jobs_bulk, name='htcondorapi-jobs-bulk'),
)


