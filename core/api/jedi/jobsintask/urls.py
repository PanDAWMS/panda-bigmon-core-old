from django.conf.urls import patterns, include, url
#from django.conf import settings
#from django.conf.urls.static import static
#from django.contrib import admin
### #FIXME admin.autodiscover()

import views as jobsintask_views

#jobsintask_views_bulk = jobsintask_views.PandaJobsViewSet.as_view(
#{
##    'post': 'addHTCondorJobs',
#    'get': 'listJobsInTask',
##    'put': 'updateHTCondorJobs',
##    'delete': 'removeHTCondorJobs',
#})

urlpatterns = patterns('',
    ### DataTables view
    url(r'^/jobsintask/$', \
        jobsintask_views.PandaJobDictJsonJobsInTask.as_view(), \
        name='api-datatables-jedi-jobs-in-task'),
    url(r'^/jobsintasksmry/$', \
        jobsintask_views.PandaJobDictJsonJobsInTaskSummary.as_view(), \
        name='api-datatables-jedi-jobs-in-task-smry'),

#    ### REST API resource
#    url(r'^jobsintask/$', jobsintask_views_bulk, name='jedi-jobs-in-task-bulk'),
)

