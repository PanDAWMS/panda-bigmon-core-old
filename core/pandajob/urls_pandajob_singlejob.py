from django.conf.urls import patterns, include, url

import views as pandajob_views

urlpatterns_pandajob_singlejob = patterns('',
###    url(r'^job$', pandajob_views.jobInfo, name='jobInfo'),
#    url(r'^job/$', pandajob_views.jobInfo, name='jobInfo'),
#    url(r'^job/(.*)/$', pandajob_views.jobInfo, name='jobInfo'),
#    url(r'^job/(.*)/(.*)/$', pandajob_views.jobInfo, name='jobInfo'),
    url(r'^$', pandajob_views.jobInfo, name='jobInfo'),
    url(r'^(.*)/$', pandajob_views.jobInfo, name='jobInfo'),
    url(r'^(.*)/(.*)/$', pandajob_views.jobInfo, name='jobInfo'),
)
urlpatterns = urlpatterns_pandajob_singlejob

