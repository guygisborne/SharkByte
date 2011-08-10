from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
	  (r'^admin/', include(admin.site.urls))
	, (r'^admin/doc/', include('django.contrib.admindocs.urls'))
	, (r'^', include('employee.urls'))
	, (r'^menu/', include('menu.urls'))
	, (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', { 'url': '/static/images/favicon.ico' }),
)

if settings.LOCAL:
	urlpatterns += patterns('', (r'^static/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': settings.MEDIA_ROOT }))
