from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

#import lsst.settings
from django.conf import settings

#import lsst.views as lsstmon_views
#import core.pandajob.views_support as core_lsstmon_support_views
#import core.pandajob.views as core_lsstmon_views

urlpatterns = patterns('',
#    url(r'^$', lsstmon_views.mainPage, name='mainPage'),
#    url(r'^jobs/$', lsstmon_views.jobList, name='jobList'),
#    url(r'^jobs/(.*)/$', lsstmon_views.jobList, name='jobList'),
#    url(r'^jobs/(.*)/(.*)/$', lsstmon_views.jobList, name='jobList'),
#    url(r'^job$', lsstmon_views.jobInfo, name='jobInfo'),
#    url(r'^job/(.*)/$', lsstmon_views.jobInfo, name='jobInfo'),
#    url(r'^job/(.*)/(.*)/$', lsstmon_views.jobInfo, name='jobInfo'),
#    url(r'^users/$', lsstmon_views.userList, name='userList'),
#    url(r'^user/(?P<user>.*)/$', lsstmon_views.userInfo, name='userInfo'),
#    url(r'^sites/$', lsstmon_views.siteList, name='siteList'),
#    url(r'^site/(?P<site>.*)/$', lsstmon_views.siteInfo, name='siteInfo'),
#    url(r'^tasks/$', lsstmon_views.taskList, name='taskList'),
#    url(r'^task$', lsstmon_views.taskInfo, name='taskInfo'),
#    url(r'^task/$', lsstmon_views.taskInfo, name='taskInfo'),
#    url(r'^task/(?P<jeditaskid>.*)/$', lsstmon_views.taskInfo, name='taskInfo'),
#    url(r'^dash/$', lsstmon_views.dashboard, name='dashboard'),
#    url(r'^dash/analysis/$', lsstmon_views.dashAnalysis, name='dashAnalysis'),
#    url(r'^dash/production/$', lsstmon_views.dashProduction, name='dashProduction'),

#    url(r'^$', core_lsstmon_views.mainPage, name='mainPage'),
#    url(r'^jobs/$', core_lsstmon_views.jobList, name='jobList'),
#    url(r'^jobs/(.*)/$', core_lsstmon_views.jobList, name='jobList'),
#    url(r'^jobs/(.*)/(.*)/$', core_lsstmon_views.jobList, name='jobList'),
#    url(r'^job$', core_lsstmon_views.jobInfo, name='jobInfo'),
#    url(r'^job/(.*)/$', core_lsstmon_views.jobInfo, name='jobInfo'),
#    url(r'^job/(.*)/(.*)/$', core_lsstmon_views.jobInfo, name='jobInfo'),
#    url(r'^users/$', core_lsstmon_views.userList, name='userList'),
#    url(r'^user/(?P<user>.*)/$', core_lsstmon_views.userInfo, name='userInfo'),
#    url(r'^sites/$', core_lsstmon_views.siteList, name='siteList'),
#    url(r'^site/(?P<site>.*)/$', core_lsstmon_views.siteInfo, name='siteInfo'),
#    url(r'^tasks/$', core_lsstmon_views.taskList, name='taskList'),
#    url(r'^task$', core_lsstmon_views.taskInfo, name='taskInfo'),
#    url(r'^task/$', core_lsstmon_views.taskInfo, name='taskInfo'),
#    url(r'^task/(?P<jeditaskid>.*)/$', core_lsstmon_views.taskInfo, name='taskInfo'),
#    url(r'^dash/$', core_lsstmon_views.dashboard, name='dashboard'),
#    url(r'^dash/analysis/$', core_lsstmon_views.dashAnalysis, name='dashAnalysis'),
#    url(r'^dash/production/$', core_lsstmon_views.dashProduction, name='dashProduction'),
    ### support views for LSST
#    url(r'^support/$', core_lsstmon_support_views.maxpandaid, name='supportRoot'),
#    url(r'^support/maxpandaid/$', core_lsstmon_support_views.maxpandaid, name='supportMaxpandaid'),

    url(r'^$', include('core.pandajob.urls_pandajob_mainpage')),
    url(r'^jobs/', include('core.pandajob.urls_pandajob_jobs')),
    url(r'^job/', include('core.pandajob.urls_pandajob_singlejob')),
    url(r'^users/', include('core.pandajob.urls_pandajob_users')),
    url(r'^user/', include('core.pandajob.urls_pandajob_singleuser')),
    url(r'^sites/', include('core.pandajob.urls_pandajob_sites')),
    url(r'^site/', include('core.pandajob.urls_pandajob_singlesite')),
    url(r'^tasks/', include('core.pandajob.urls_pandajob_tasks')),
    url(r'^task/', include('core.pandajob.urls_pandajob_singletask')),
    url(r'^dash/', include('core.pandajob.urls_pandajob_dash')),
    url(r'^support/', include('core.pandajob.urls_pandajob_support')),


    ### robots.txt
    url('^robots\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),

) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


#urlpatterns += common_patterns
#urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
