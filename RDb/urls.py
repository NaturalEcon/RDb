from django.conf.urls import patterns, include, url
from RDb import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^RDb/', include('RDb.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
