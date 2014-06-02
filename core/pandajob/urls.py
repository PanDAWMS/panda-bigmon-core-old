from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
### #FIXME admin.autodiscover()

import views as pandajob_views

urlpatterns = patterns('',
    ### PanDA jobs
#    url(r'^/$', pandajob_views.listJobs, name='jobIndex'),
#    url(r'^/list/$', pandajob_views.listJobs, name='jobList'),
#    url(r'^/list3/$', pandajob_views.list3PandaJobs, name='jobList'),
#    url(r'^/(?P<pandaid>\d+)/$', pandajob_views.jobDetails, name='jobDetails'),
#    url(r'^/info/(?P<prodUserName>[-A-Za-z0-9_.+ @]+)/(?P<nhours>\d+)/$', pandajob_views.jobInfoOrig, name='jobInfo'),
#    url(r'^/info/d/(?P<prodUserName>[-A-Za-z0-9_.+ @]+)/(?P<ndays>\d+)/$', pandajob_views.jobInfoDaysOrig, name='jobInfoDays'),
#    url(r'^/info/h/(?P<prodUserName>[-A-Za-z0-9_.+ @]+)/(?P<nhours>\d+)/$', pandajob_views.jobInfoHoursOrig, name='jobInfoHours'),
    url(r'^/info/$', pandajob_views.jobInfoDefaultOrig, name='jobInfoDefault'),
#    url(r'^/task/$', pandajob_views.jediJobsInTask, name='jediJobsInTask'),

#    ### backported from LSST
    url(r'^/', include('core.pandajob.urls_pandajob_mainpage'), name='namespace_mainpage'),
    url(r'^jobs/', include('core.pandajob.urls_pandajob_jobs'), name='namespace_jobs'),
    url(r'^job/', include('core.pandajob.urls_pandajob_singlejob'), name='namespace_job'),
    url(r'^users/', include('core.pandajob.urls_pandajob_users'), name='namespace_users'),
    url(r'^user/', include('core.pandajob.urls_pandajob_singleuser'), name='namespace_user'),
    url(r'^sites/', include('core.pandajob.urls_pandajob_sites'), name='namespace_sites'),
    url(r'^site/', include('core.pandajob.urls_pandajob_singlesite'), name='namespace_site'),
    url(r'^tasks/', include('core.pandajob.urls_pandajob_tasks'), name='namespace_tasks'),
    url(r'^task/', include('core.pandajob.urls_pandajob_singletask'), name='namespace_task'),
    url(r'^dash/', include('core.pandajob.urls_pandajob_dash'), name='namespace_dash'),
    url(r'^support/', include('core.pandajob.urls_pandajob_support'), name='namespace_support'),

)


