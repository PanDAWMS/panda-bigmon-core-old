from django.conf.urls import patterns, include, url
#from django.conf import settings
#from django.conf.urls.static import static
#from django.contrib import admin

import views_users as users_views

urlpatterns = patterns('',
    ### PanDA Users
    url(r'^/$', users_views.listActiveUsers, name='listusers'),
    url(r'^/(?P<produsername>[-A-Za-z0-9_.+ @]+)/$', users_views.userActivity, name='useractivity'),
#    url(r'^/(?P<produsername>[-A-Za-z0-9_.+ @]+)/(?P<jobsetid>\d+)/$', users_views.jediUserJobset, name='userjobset'),
)


