from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
from django.views.generic.simple import direct_to_template

admin.autodiscover()

urlpatterns = patterns('',
		       (r'^admin/doc/', include('django.contrib.admindocs.urls')),
		       (r'^admin/', include(admin.site.urls)),

		       (r'^order/', 'employee.views.menuForToday'),
		       (r'^createMeal/', 'menu.views.createMeal'),
		       (r'^createMenu/', 'menu.views.createMenu'),


		       #(r'^', include('general.urls')),
		       #(r'^calendar/', include('cal.urls')),
)

if settings.LOCAL:
	urlpatterns += patterns('',
				(r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.MEDIA_ROOT})
)
