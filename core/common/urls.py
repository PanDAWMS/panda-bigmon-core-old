from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
### #FIXME admin.autodiscover()

import views as common_views
#from ..table import views as table_views
from ..pandajob import views as pandajob_views
from ..htcondor import views as htcondor_views
#from ..resource import views as resource_views
#from ..table import views as table_views
#from ..graphics import views as graphics_views
#from ..task import views as task_views



common_patterns = patterns('',
    ### the front page
    url(r'^$', common_views.index, name='index'),


    ### Applications
    url(r'^htcondorjobs', include('core.htcondor.urls')),
    url(r'^job', include('core.pandajob.urls')),
    url(r'^resource', include('core.resource.urls')),
    url(r'^api-auth', include('core.api.urls')),


    ### UI elements
    url(r'^api/datatables', include('core.table.urls')),
#    url(r'^graphics/', include('core.graphics.urls')),
#    url(r'^task/', include('core.task.urls')),


    ### TEST/Playground
    url(r'^test_playground/$', common_views.testing, name='testing'),
    url(r'^htc4/$', htcondor_views.list3HTCondorJobs, name='htc4'),
    url(r'^pan4/$', pandajob_views.list3PandaJobs, name='pan4'),


    ### Django Admin
    ### Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    ### Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),


) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


urlpatterns = patterns('',)
urlpatterns += common_patterns
