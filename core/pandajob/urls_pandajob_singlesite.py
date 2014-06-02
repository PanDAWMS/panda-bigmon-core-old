from django.conf.urls import patterns, include, url

import views as pandajob_views

urlpatterns_pandajob_singlesite = patterns('',
#    url(r'^site/(?P<site>.*)/$', pandajob_views.siteInfo, name='siteInfo'),
    url(r'^(?P<site>.*)/$', pandajob_views.siteInfo, name='siteInfo'),
)
urlpatterns = urlpatterns_pandajob_singlesite

