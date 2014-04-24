from django.conf.urls import patterns, include, url
#from django.conf import settings
#from django.conf.urls.static import static
#from django.contrib import admin
### #FIXME admin.autodiscover()

import views as user_views

urlpatterns = patterns('',
    ### DataTables view
    url(r'^/listactive/$', \
        user_views.ListActiveUsersDictJson.as_view(), \
        name='api-datatables-user-list-active-users'),
    url(r'^/useractivity/$', \
        user_views.ListUsersActivityDictJson.as_view(), \
        name='api-datatables-user-list-user-activity'),
    url(r'^/useractivitysmry/$', \
        user_views.ListUsersActivitySmryDictJson.as_view(), \
        name='api-datatables-user-list-user-activity-smry'),
)


