from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

#from core.common.urls import *

import lsst.settings

import lsst.views as lsstmon_views

urlpatterns = patterns('',
    url(r'^$', lsstmon_views.mainPage),
    url(r'^lsst/$', lsstmon_views.mainPage, name='mainPage'),
    url(r'^lsst/jobs/$', lsstmon_views.jobList, name='jobList'),
    url(r'^lsst/jobs/(.*)/$', lsstmon_views.jobList, name='jobList'),
    url(r'^lsst/jobs/(.*)/(.*)/$', lsstmon_views.jobList, name='jobList'),
    url(r'^lsst/job$', lsstmon_views.jobInfo, name='jobInfo'),
    url(r'^lsst/job/(?P<pandaid>.*)/$', lsstmon_views.jobInfo, name='jobInfo'),
    url(r'^lsst/job/(.*)/$', lsstmon_views.jobInfo, name='jobInfo'),
    url(r'^lsst/job/(.*)/(.*)/$', lsstmon_views.jobInfo, name='jobInfo'),
    url(r'^lsst/users/$', lsstmon_views.userList, name='userList'),
    url(r'^lsst/user/(?P<user>.*)/$', lsstmon_views.userInfo, name='userInfo'),
    url(r'^lsst/sites/$', lsstmon_views.siteList, name='siteList'),
    url(r'^lsst/site/(?P<site>.*)/$', lsstmon_views.siteInfo, name='siteInfo'),
    url(r'^lsst/tasks/$', lsstmon_views.taskList, name='taskList'),
    url(r'^lsst/task$', lsstmon_views.taskInfo, name='taskInfo'),
    url(r'^lsst/task/$', lsstmon_views.taskInfo, name='taskInfo'),
    url(r'^lsst/task/(?P<jeditaskid>.*)/$', lsstmon_views.taskInfo, name='taskInfo'),
    url(r'^lsst/dash/$', lsstmon_views.dashboard, name='dashboard'),
    url(r'^lsst/dash/analysis/$', lsstmon_views.dashAnalysis, name='dashAnalysis'),
    url(r'^lsst/dash/production/$', lsstmon_views.dashProduction, name='dashProduction'),

    ### robots.txt
    url('^robots\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),

) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


#urlpatterns += common_patterns
#urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

