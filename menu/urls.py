from django.conf.urls.defaults import *

from views import *

urlpatterns = patterns('kitchen.menu.views',
	url(r'^order/$', 'order', name='order'), 
)
