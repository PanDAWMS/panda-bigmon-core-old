from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

#import lsst.settings
from django.conf import settings

import common_views as lsstmon_views
#import lsst.views as lsstmon_views
import core.pandajob.views_support as core_lsstmon_support_views
#import core.pandajob.views as core_lsstmon_views
#import core.api.reprocessing.views as core_lsstmon_api_reprocessing_views

urlpatterns = patterns('',
    url(r'^$', lsstmon_views.mainPage, name='mainPage'),
    url(r'^$', lsstmon_views.mainPage, name='index'),
    url(r'^help/$', lsstmon_views.helpPage, name='helpPage'),
    url(r'^jobs/$', lsstmon_views.jobList, name='jobList'),
    url(r'^jobs/(.*)/$', lsstmon_views.jobList, name='jobList'),
    url(r'^jobs/(.*)/(.*)/$', lsstmon_views.jobList, name='jobList'),
    url(r'^job$', lsstmon_views.jobInfo, name='jobInfo'),
    url(r'^job/(.*)/$', lsstmon_views.jobInfo, name='jobInfo'),
    url(r'^job/(.*)/(.*)/$', lsstmon_views.jobInfo, name='jobInfo'),
    url(r'^users/$', lsstmon_views.userList, name='userList'),
    url(r'^user/(?P<user>.*)/$', lsstmon_views.userInfo, name='userInfo'),
    url(r'^user/$', lsstmon_views.userInfo, name='userInfo'),
    url(r'^sites/$', lsstmon_views.siteList, name='siteList'),
    url(r'^site/(?P<site>.*)/$', lsstmon_views.siteInfo, name='siteInfo'),
    url(r'^site/$', lsstmon_views.siteInfo, name='siteInfo'),
    url(r'^wns/(?P<site>.*)/$', lsstmon_views.wnInfo, name='wnInfo'),
    url(r'^wn/(?P<site>.*)/(?P<wnname>.*)/$', lsstmon_views.wnInfo, name='wnInfo'),
    url(r'^tasks/$', lsstmon_views.taskList, name='taskList'),
    url(r'^task$', lsstmon_views.taskInfo, name='taskInfo'),
    url(r'^task/$', lsstmon_views.taskInfo, name='taskInfo'),
    url(r'^errors/$', lsstmon_views.errorSummary, name='errorSummary'),
    url(r'^incidents/$', lsstmon_views.incidentList, name='incidentList'),
    url(r'^logger/$', lsstmon_views.pandaLogger, name='pandaLogger'),
    url(r'^task/(?P<jeditaskid>.*)/$', lsstmon_views.taskInfo, name='taskInfo'),
    url(r'^dash/$', lsstmon_views.dashboard, name='dashboard'),
    url(r'^dash/analysis/$', lsstmon_views.dashAnalysis, name='dashAnalysis'),
    url(r'^dash/production/$', lsstmon_views.dashProduction, name='dashProduction'),
    url(r'^workingGroups/$', lsstmon_views.workingGroups, name='workingGroups'),
    url(r'^fileInfo/$', lsstmon_views.fileInfo, name='fileInfo'),
    url(r'^fileList/$', lsstmon_views.fileList, name='fileList'),
    url(r'^datasetInfo/$', lsstmon_views.datasetInfo, name='datasetInfo'),
    url(r'^datasetList/$', lsstmon_views.datasetList, name='datasetList'),
    url(r'^workQueues/$', lsstmon_views.workQueues, name='workQueues'),

    ### support views for LSST
    url(r'^support/$', core_lsstmon_support_views.maxpandaid, name='supportRoot'),
    url(r'^support/maxpandaid/$', core_lsstmon_support_views.maxpandaid, name='supportMaxpandaid'),
    url(r'^support/jobinfouservohrs/(?P<vo>[-A-Za-z0-9_.+ @]+)/(?P<nhours>\d+)/$', core_lsstmon_support_views.jobUserOrig, name='supportJobUserVoHrs'),
    url(r'^support/jobinfouservo/(?P<vo>[-A-Za-z0-9_.+ @]+)/(?P<ndays>\d+)/$', core_lsstmon_support_views.jobUserDaysOrig, name='supportJobUserVo'),


    ### api
    url(r'^api/$', core_lsstmon_support_views.maxpandaid, name='supportRoot'),
    url(r'^api/reprocessing/$', include('core.api.reprocessing.urls')),


    ### robots.txt
    url('^robots\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),

) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


#urlpatterns += common_patterns
#urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
