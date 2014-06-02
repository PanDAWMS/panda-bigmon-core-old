from django.conf.urls import patterns, include, url

import views as pandajob_views

urlpatterns_pandajob_singletask = patterns('',
##    url(r'^task$', pandajob_views.taskInfo, name='taskInfo'),
#    url(r'^task/$', pandajob_views.taskInfo, name='taskInfo'),
#    url(r'^task/(?P<jeditaskid>.*)/$', pandajob_views.taskInfo, name='taskInfo'),
    url(r'^$', pandajob_views.taskInfo, name='taskInfo'),
    url(r'^(?P<jeditaskid>.*)/$', pandajob_views.taskInfo, name='taskInfo'),
)
urlpatterns = urlpatterns_pandajob_singletask

