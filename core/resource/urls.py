from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
### #FIXME admin.autodiscover()

import views as resource_views

urlpatterns = patterns('',
    ### Schedconfig
### Disabled on purpose: ###    url(r'^update/(?P<vo>\w+)/$', resource_views.updateSchedconfig, name='updateSchedconfig'),
    url(r'^/$', resource_views.listSchedconfigQueues, name='listSchedconfigQueues'),
    url(r'^/(?P<nickname>[-A-Za-z0-9_]+)/$', resource_views.schedconfigDetails, name='schedconfigDetails'),
)


