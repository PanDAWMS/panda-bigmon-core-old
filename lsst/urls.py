from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

#from core.common.urls import *

import lsst.settings

import lsst.views as lsstmon_views

urlpatterns = patterns('',
###     url(r'^$', lsstmon_views.mainPage),
###     url(r'^lsst/$', lsstmon_views.mainPage),
###     url(r'^lsst/jobs/$', lsstmon_views.jobList),
###     url(r'^lsst/jobs/(.*)/$', lsstmon_views.jobList),
###     url(r'^lsst/jobs/(.*)/(.*)/$', lsstmon_views.jobList),
###     url(r'^lsst/job$', lsstmon_views.jobInfo),
###     url(r'^lsst/job/(.*)/$', lsstmon_views.jobInfo),
###     url(r'^lsst/job/(.*)/(.*)/$', lsstmon_views.jobInfo),
###     url(r'^lsst/users/$', lsstmon_views.userList),
###     url(r'^lsst/user/(?P<user>.*)/$', lsstmon_views.userInfo),
###     url(r'^lsst/sites/$', lsstmon_views.siteList),
###     url(r'^lsst/site/(?P<site>.*)/$', lsstmon_views.siteInfo),
#    url(r'^$', lsstmon_views.mainPage),
    url(r'^$', lsstmon_views.mainPage),
    url(r'^jobs/$', lsstmon_views.jobList),
    url(r'^jobs/(.*)/$', lsstmon_views.jobList),
    url(r'^jobs/(.*)/(.*)/$', lsstmon_views.jobList),
    url(r'^job$', lsstmon_views.jobInfo),
    url(r'^job/(.*)/$', lsstmon_views.jobInfo),
    url(r'^job/(.*)/(.*)/$', lsstmon_views.jobInfo),
    url(r'^users/$', lsstmon_views.userList),
    url(r'^user/(?P<user>.*)/$', lsstmon_views.userInfo),
    url(r'^sites/$', lsstmon_views.siteList),
    url(r'^site/(?P<site>.*)/$', lsstmon_views.siteInfo),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


#urlpatterns += common_patterns
#urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

