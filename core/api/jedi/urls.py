"""
api.jedi.urls

 
"""

from django.conf.urls import patterns, include, url


common_patterns = patterns('',
    ### Applications
    url(r'^jobsInTask/$', include('core.api.jedi.jobsintask.urls')),

)


urlpatterns = patterns('',)
urlpatterns += common_patterns


