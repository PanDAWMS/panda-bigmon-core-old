from django.conf.urls import patterns, include, url

import views as pandajob_views

urlpatterns_pandajob_singleuser = patterns('',
#    url(r'^user/(?P<user>.*)/$', pandajob_views.userInfo, name='userInfo'),
    url(r'^(?P<user>.*)/$', pandajob_views.userInfo, name='userInfo'),
)
urlpatterns = urlpatterns_pandajob_singleuser

