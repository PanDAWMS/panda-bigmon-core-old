"""
    api.reprocessing.urls
"""
from django.conf.urls import patterns, include, url
#from django.conf import settings
#from django.conf.urls.static import static
#from django.contrib import admin
### #FIXME admin.autodiscover()

import views as reprocessing_views

urlpatterns = patterns('',
    ### DataTables view
    url(r'^$', \
        reprocessing_views.PandaJobDictJsonReprocessingSmryPage.as_view(), \
        name='api-reprocessing-jobs-in-task-smry'),
)

