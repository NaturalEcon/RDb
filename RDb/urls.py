from django.conf.urls import patterns, include, url
from RDb import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
admin.autodiscover()

uuid_re = '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'

rviewstring = '^resource/(?P<ner_uuid>%s)/$' % uuid_re

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^resource_list/',views.resource_list, name='resource_list'),
    url(rviewstring, views.resource_view, name='resource'),
    url(r'^actor/(?P<neactor_id>\d+)/$', views.neactor, name='actor'),
    url(r'^process/(?P<neprocess_id>\d+)/$', views.neactor, name='process'),
    url(r'^surveyvalue/(?P<sv_id>\d+)/$', views.nesurveyvalue, name='surveyvalue'),
    url(r'^surveyinfo/(?P<si_id>\d+)/$', views.nesurveyinfo, name='surveyinfo'),
#    url(r'^collection/(?P<necollection_id>\d+)/$', views.necollection, name='collection'),
#    url(r'^dependency/(?P<nedependency_id>\d+)/$', views.nedependency, name='dependency'),
) 