from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect

from models import *

def order(request):
	return render_to_response('order.html', {}, context_instance=RequestContext(request))

def menuList(request):
	if not request.user.is_authenticated() or not request.user.is_staff:
		return HttpResponseRedirect('/admin/') 

	return render_to_response('menu_list.html', {}, context_instance=RequestContext(request))

def orderList(request, menuID):
	if not request.user.is_authenticated() or not request.user.is_staff:
		return HttpResponseRedirect('/admin/')

	return render_to_response('order_list.html', { 'menuID': menuID }, context_instance=RequestContext(request))

