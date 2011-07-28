from django.conf.urls.defaults import *

from views import *

urlpatterns = patterns('menu.views',
	url(r'^order/$', 'order', name='order'), 
	url(r'^menu-list/$', 'menuList', name='menu-list'), 
	url(r'^order-list/(?P<menuID>\d+)/$', 'orderList', name='order-list'), 
)
