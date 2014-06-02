from django.conf.urls import patterns, include, url

import views as pandajob_views

urlpatterns_pandajob_users = patterns('',
#    url(r'^users/$', pandajob_views.userList, name='userList'),
    url(r'^$', pandajob_views.userList, name='userList'),
)
urlpatterns = urlpatterns_pandajob_users

