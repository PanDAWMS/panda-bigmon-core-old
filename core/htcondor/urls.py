from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
### #FIXME admin.autodiscover()

import views as htcondor_views
#from ..api.htcondorapi import views as htcondorapi_views

urlpatterns = patterns('',
    ### HTCondor Jobs
    url(r'^/$', htcondor_views.list3HTCondorJobs, name='listHTCondorJobs'),
    url(r'^/(?P<globaljobid>[-A-Za-z0-9_.#]+)/$', htcondor_views.htcondorJobDetails, name='HTCondorJobDetails'),
)


