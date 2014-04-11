"""
api.urls

 
"""
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
### #FIXME admin.autodiscover()


common_patterns = patterns('',
    ### Applications
    url(r'^htcondor', include('core.api.htcondorapi.urls')),
    url(r'^jedi', include('core.api.jedi.urls')),

)

urlpatterns = patterns('',)
urlpatterns += common_patterns


