from django.conf.urls.defaults import *

from views import *

urlpatterns = patterns('kitchen.employee.views',
	url(r'^$', 'login', name='login'), 
	url(r'^logout/$', 'logout', name='logout'),
	url(r'^authenticate/$', 'authenticate', name='authenticate'), 
	url(r'^profile/$', 'profile', name='profile'), 
)
