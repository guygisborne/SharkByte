from django.conf.urls.defaults import *

from views import *

urlpatterns = patterns('employee.views',
	  url(r'^$', 'login', name='login')
	, url(r'^logout/$', 'logout', name='logout')
	, url(r'^authenticate/$', 'authenticate', name='authenticate')
	, url(r'^edit-profile/$', 'edit_profile', name='edit_profile') 
)
