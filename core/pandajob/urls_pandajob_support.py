from django.conf.urls import patterns, include, url

import views_support as pandajob_support_views

urlpatterns_pandajob_users = patterns('',
#    url(r'^support/$', pandajob_support_views.maxpandaid, name='supportRoot'),
#    url(r'^support/maxpandaid/$', pandajob_support_views.maxpandaid, name='supportMaxpandaid'),
    url(r'^$', pandajob_support_views.maxpandaid, name='supportRoot'),
    url(r'^maxpandaid/$', pandajob_support_views.maxpandaid, name='supportMaxpandaid'),
    url(r'^jobinfouservohrs/(?P<vo>[-A-Za-z0-9_.+ @]+)/(?P<nhours>\d+)/$', core_lsstmon_support_views.jobUserOrig, name='supportJobUserVoHrs'),
    url(r'^jobinfouservo/(?P<vo>[-A-Za-z0-9_.+ @]+)/(?P<ndays>\d+)/$', pandajob_support_views.jobUserDaysOrig, name='supportJobUserVo'),
)
urlpatterns = urlpatterns_pandajob_users

