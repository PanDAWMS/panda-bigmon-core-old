from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
### #FIXME admin.autodiscover()

from core import views as core_views
from topology import views as topology_views
from htcondor import views as htcondor_views
from api.htcondorapi import views as htcondorapi_views

#### Actions of HTCondor API
htcondorapi_addjob = htcondorapi_views.HTCondorJobsViewSet.as_view(
{
    'get': 'list',
    'post': 'addHTCondorJobs',
})
htcondorapi_updatejob = htcondorapi_views.HTCondorJobsViewSet.as_view(
{
    'get': 'list',
    'post': 'updateHTCondorJobs',
})
htcondorapi_removejob = htcondorapi_views.HTCondorJobsViewSet.as_view(
{
    'get': 'list',
    'post': 'removeHTCondorJobs',
})
htcondorapi_listjob = htcondorapi_views.HTCondorJobsViewSet.as_view(
{
    'get': 'listForDataTables',
})

urlpatterns = patterns('',
    ### the front page
    url(r'^$', core_views.index, name='index'),

    ### PanDA jobs
    url(r'^job/list/$', core_views.listJobs, name='jobList'),
    url(r'^job/$', core_views.listJobs, name='jobList2'),
    url(r'^job/(?P<pandaid>\d+)/$', core_views.jobDetails, name='jobDetails'),
    url(r'^job/info/(?P<prodUserName>[-A-Za-z0-9_.+ ]+)/(?P<ndays>\d+)/$', core_views.jobInfo, name='jobInfo'),
    url(r'^job/info/$', core_views.jobInfoDefault, name='jobInfoDefault'),


    ### Schedconfig
### Disabled on purpose: ###    url(r'^update_schedconfig/(?P<vo>\w+)/$', topology_views.updateSchedconfig, name='updateSchedconfig'),
    url(r'^schedconfig/$', topology_views.listSchedconfigQueues, name='listSchedconfigQueues'),
    url(r'^schedconfig/(?P<nickname>[-A-Za-z0-9_]+)/$', topology_views.schedconfigDetails, name='schedconfigDetails'),


    ### HTCondor Jobs
    url(r'^htcondorjobs/$', htcondor_views.list3HTCondorJobs, name='listHTCondorJobs'),
    url(r'^htcondorjobs/(?P<globaljobid>[-A-Za-z0-9_.#]+)/$', htcondor_views.htcondorJobDetails, name='HTCondorJobDetails'),


    ### REST framework API
    url(r'^api-auth/htcondorapi/addjob/$', htcondorapi_addjob, name='htcondorapi-add-job'),
    url(r'^api-auth/htcondorapi/updatejob/$', htcondorapi_updatejob, name='htcondorapi-update-job'),
    url(r'^api-auth/htcondorapi/removejob/$', htcondorapi_removejob, name='htcondorapi-remove-job'),
    url(r'^api/listall/htcondor/$', htcondorapi_listjob, name='api-datatables-htcondor-dict'),


    ### dataTables food
    url(r'^api/datatables/htcondorjob/$', htcondor_views.HTCondorJobDictJson.as_view(), name='api-datatables-htcondor-jobs'),
    url(r'^api/datatables/pandajob/$', core_views.PandaJobDictJson.as_view(), name='api-datatables-panda-jobs'),


    ### TEST/Playground
    url(r'^test_playground/$', core_views.testing, name='testing'),
    url(r'^htc4/$', htcondor_views.list3HTCondorJobs, name='htc4'),
    url(r'^pan4/$', core_views.list3PandaJobs, name='pan4'),

    ### Django Admin
    ### Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    ### Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),


) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


