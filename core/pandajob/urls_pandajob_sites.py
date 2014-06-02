from django.conf.urls import patterns, include, url

import views as pandajob_views

urlpatterns_pandajob_sites = patterns('',
#    url(r'^sites/$', pandajob_views.siteList, name='siteList'),
    url(r'^$', pandajob_views.siteList, name='siteList'),
)
urlpatterns = urlpatterns_pandajob_sites

