from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
### #FIXME admin.autodiscover()

import views as pandajob_views

urlpatterns = patterns('',
    ### PanDA jobs
    url(r'^/$', pandajob_views.listJobs, name='jobIndex'),
    url(r'^/list/$', pandajob_views.listJobs, name='jobList'),
    url(r'^/(?P<pandaid>\d+)/$', pandajob_views.jobDetails, name='jobDetails'),
    url(r'^/info/(?P<prodUserName>[-A-Za-z0-9_.+ @]+)/(?P<nhours>\d+)/$', pandajob_views.jobInfo, name='jobInfo'),
    url(r'^/info/d/(?P<prodUserName>[-A-Za-z0-9_.+ @]+)/(?P<ndays>\d+)/$', pandajob_views.jobInfoDays, name='jobInfoDays'),
    url(r'^/info/h/(?P<prodUserName>[-A-Za-z0-9_.+ @]+)/(?P<nhours>\d+)/$', pandajob_views.jobInfoHours, name='jobInfoHours'),
    url(r'^/info/$', pandajob_views.jobInfoDefault, name='jobInfoDefault'),
    url(r'^/task/$', pandajob_views.jediJobsInTask, name='jediJobsInTask'),
)


