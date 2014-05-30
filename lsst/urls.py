from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

#from core.common.urls import *

import lsst.settings

import lsst.views as lsstmon_views

urlpatterns = patterns('',
    url(r'^$', lsstmon_views.mainPage, name='mainPage'),
    url(r'^jobs/$', lsstmon_views.jobList, name='jobList'),
    url(r'^jobs/(.*)/$', lsstmon_views.jobList, name='jobList'),
    url(r'^jobs/(.*)/(.*)/$', lsstmon_views.jobList, name='jobList'),
    url(r'^job$', lsstmon_views.jobInfo, name='jobInfo'),
    url(r'^job/(.*)/$', lsstmon_views.jobInfo, name='jobInfo'),
    url(r'^job/(.*)/(.*)/$', lsstmon_views.jobInfo, name='jobInfo'),
    url(r'^users/$', lsstmon_views.userList, name='userList'),
    url(r'^user/(?P<user>.*)/$', lsstmon_views.userInfo, name='userInfo'),
    url(r'^sites/$', lsstmon_views.siteList, name='siteList'),
    url(r'^site/(?P<site>.*)/$', lsstmon_views.siteInfo, name='siteInfo'),
    url(r'^tasks/$', lsstmon_views.taskList, name='taskList'),
    url(r'^task$', lsstmon_views.taskInfo, name='taskInfo'),
    url(r'^task/$', lsstmon_views.taskInfo, name='taskInfo'),
    url(r'^task/(?P<jeditaskid>.*)/$', lsstmon_views.taskInfo, name='taskInfo'),
    url(r'^dash/$', lsstmon_views.dashboard, name='dashboard'),
    url(r'^dash/analysis/$', lsstmon_views.dashAnalysis, name='dashAnalysis'),
    url(r'^dash/production/$', lsstmon_views.dashProduction, name='dashProduction'),

    ### robots.txt
    url('^robots\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),

) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


#urlpatterns += common_patterns
#urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
