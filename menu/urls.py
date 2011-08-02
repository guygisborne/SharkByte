from django.conf.urls.defaults import *

from views import *

urlpatterns = patterns('menu.views',
	url(r'^order/$', 'order', name='order'), 
	url(r'^order/place/(?P<menuID>\d+)/$', 'placeOrder', name='place'), 
	url(r'^order/confirm/(?P<orderID>\d+)/$', 'confirmOrder', name='confirm'), 
	url(r'^order/cancel/(?P<orderID>\d+)/$', 'cancelOrder', name='cancel'), 
	url(r'^menu-list/$', 'menuList', name='menu-list'), 
	url(r'^order-list/(?P<menuID>\d+)/$', 'orderList', name='order-list'), 
)
