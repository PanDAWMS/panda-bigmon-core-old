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

    url(r'^/$', pandajob_views.mainPage, name='mainPage'),
    url(r'^jobs/$', pandajob_views.jobList, name='jobList'),
    url(r'^jobs/(.*)/$', pandajob_views.jobList, name='jobList'),
    url(r'^jobs/(.*)/(.*)/$', pandajob_views.jobList, name='jobList'),
###    url(r'^job$', pandajob_views.jobInfo, name='jobInfo'),
    url(r'^job/$', pandajob_views.jobInfo, name='jobInfo'),
    url(r'^job/(.*)/$', pandajob_views.jobInfo, name='jobInfo'),
    url(r'^job/(.*)/(.*)/$', pandajob_views.jobInfo, name='jobInfo'),
    url(r'^users/$', pandajob_views.userList, name='userList'),
    url(r'^user/(?P<user>.*)/$', pandajob_views.userInfo, name='userInfo'),
    url(r'^sites/$', pandajob_views.siteList, name='siteList'),
    url(r'^site/(?P<site>.*)/$', pandajob_views.siteInfo, name='siteInfo'),
    url(r'^tasks/$', pandajob_views.taskList, name='taskList'),
#    url(r'^task$', pandajob_views.taskInfo, name='taskInfo'),
    url(r'^task/$', pandajob_views.taskInfo, name='taskInfo'),
    url(r'^task/(?P<jeditaskid>.*)/$', pandajob_views.taskInfo, name='taskInfo'),
    url(r'^dash/$', pandajob_views.dashboard, name='dashboard'),
    url(r'^dash/analysis/$', pandajob_views.dashAnalysis, name='dashAnalysis'),
    url(r'^dash/production/$', pandajob_views.dashProduction, name='dashProduction'),

)


