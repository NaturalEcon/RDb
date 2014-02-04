from django.conf.urls import patterns, include, url
from RDb import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static 
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'views.index', name='index'),
    url(r'^RDb/', include('RDb.urls')),
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
