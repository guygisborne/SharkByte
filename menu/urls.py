from django.conf.urls.defaults import *

from views import *

urlpatterns = patterns('menu.views',
	  url(r'^order-list/$', 'order_list', name='order_list') 
	, url(r'^order-list/create/(?P<menu_id>\d+)/$', 'create_order', name='create_order')
	, url(r'^order-list/confirm/(?P<order_id>\d+)/$', 'confirm_order', name='confirm_order')
	, url(r'^order-list/cancel/(?P<order_id>\d+)/$', 'cancel_order', name='cancel_order')
	, url(r'^menu-list/$', 'menu_list', name='menu_list')
	, url(r'^menu-list/(?P<menu_id>\d+)/$', 'orders_for_menu', name='orders_for_menu'),
)
