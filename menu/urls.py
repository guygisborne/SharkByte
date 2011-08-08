from django.conf.urls.defaults import *

from views import *

urlpatterns = patterns('menu.views',
	  url(r'^todays/$', 'todays_menu', name='todays_menu') 
	, url(r'^todays/create/(?P<menu_id>\d+)/$', 'create_order', name='create_order')
	, url(r'^todays/confirm/(?P<order_id>\d+)/$', 'confirm_order', name='confirm_order')
	, url(r'^todays/cancel/(?P<order_id>\d+)/$', 'cancel_order', name='cancel_order')
	, url(r'^menu-list/$', 'menu_list', name='menu_list')
	, url(r'^menu-list/(?P<menu_id>\d+)/$', 'order_list', name='order_list')
	, url(r'^menu-list/(?P<menu_id>\d+)/get-orders/$', 'get_orders', name='get_orders')
	, url(r'^menu-list/(?P<menu_id>\d+)/fulfill-orders/$', 'fulfill_orders', name='fulfill_orders')
)
