from django.conf.urls import patterns, include, url

import views as pandajob_views

urlpatterns_pandajob_dashboard = patterns('',
#    url(r'^dash/$', pandajob_views.dashboard, name='dashboard'),
#    url(r'^dash/analysis/$', pandajob_views.dashAnalysis, name='dashAnalysis'),
#    url(r'^dash/production/$', pandajob_views.dashProduction, name='dashProduction'),
    url(r'^$', pandajob_views.dashboard, name='dashboard'),
    url(r'^analysis/$', pandajob_views.dashAnalysis, name='dashAnalysis'),
    url(r'^production/$', pandajob_views.dashProduction, name='dashProduction'),
)
urlpatterns = urlpatterns_pandajob_dashboard

