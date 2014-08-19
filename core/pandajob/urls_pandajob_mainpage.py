from django.conf.urls import patterns, include, url

import views as pandajob_views

urlpatterns_pandajob_mainpage = patterns('',
    ### backported from LSST
    url(r'^$', pandajob_views.mainPage, name='index'),
)
urlpatterns = urlpatterns_pandajob_mainpage

