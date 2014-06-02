from django.conf.urls import patterns, include, url

import views as pandajob_views

urlpatterns_pandajob_tasks = patterns('',
    url(r'^$', pandajob_views.taskList, name='taskList'),
)
urlpatterns = urlpatterns_pandajob_tasks

