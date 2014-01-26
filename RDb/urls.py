from django.conf.urls import patterns, include, url
from RDb.views import ResourceListView, ResourceDetailView, ActorListView,ActorDetailView,\
    ProcessListView,ProcessDetailView, SurveyDetailView, SurveyInfoDetailView, index
from django.contrib import admin
#from django.conf import settings
#from django.conf.urls.static import static
admin.autodiscover()

uuid_re = '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'


urlpatterns = patterns('',
    url(r'^$', index, name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^resource_list/',ResourceListView.as_view(), name='resource_list'),
    url(r'^actor_list/',ActorListView.as_view(), name='actor_list'),
    url(r'^process_list/',ProcessListView.as_view(), name='process_list'),
    url(r'^resource/(?P<pk>%s)/$' % uuid_re, ResourceDetailView.as_view(), name='resource'),
    url(r'^details/(?P<pk>\d+)/$', ActorDetailView.as_view(), name='actor'),
    url(r'^process/(?P<pk>\d+)/$', ProcessDetailView.as_view(), name='process'),
    url(r'^surveyvalue/(?P<pk>\d+)/$', SurveyDetailView.as_view(), name='surveyvalue'),
    url(r'^surveyinfo/(?P<pk>\d+)/$', SurveyInfoDetailView.as_view(), name='surveyinfo'),
#    url(r'^collection/(?P<necollection_id>\d+)/$', views.necollection, name='collection'),
#    url(r'^dependency/(?P<nedependency_id>\d+)/$', views.nedependency, name='dependency'),
) 