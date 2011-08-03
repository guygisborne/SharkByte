from datetime import date, datetime
import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib import auth

from models import *
from forms import *
from employee.models import *

def employee_required(viewFn):
	def decorated(request, *args, **kwargs):
		if 'employeeID' not in request.session:
			return HttpResponseRedirect(reverse('login'))
		else:
			return viewFn(request, *args, **kwargs)
	return decorated

def post_required(redirect):
	def decorator(viewFn):
		def decorated(request, *args, **kwargs):
			if request.method != 'POST':
				return HttpResponseRedirect(reverse(redirect))
			else:
				return viewFn(request, *args, **kwargs)
		return decorated
	return decorator

@employee_required
def order(request, prevOrder=None):
	employee = get_object_or_404(Employee, pk=request.session['employeeID'])
	menus = Menu.managed.todaysMenus(employee)

	for menu in menus:
		menu['form'] = OrderForm(menu['menu'], instance=prevOrder) if menu['menu'] else False

	return render_to_response('order.html', { 'menus': menus }, context_instance=RequestContext(request))

@employee_required
def cancelOrder(request, orderID):
	employee = get_object_or_404(Employee, pk=request.session['employeeID'])
	order = get_object_or_404(Order, pk=orderID, employee=employee)
	order.delete()
	return HttpResponseRedirect(reverse('order'))

@employee_required
def confirmOrder(request, orderID):
	employee = get_object_or_404(Employee, pk=request.session['employeeID'])
	order = get_object_or_404(Order, pk=orderID, employee=employee)

	if order.isConfirmable():
		order.confirm()
	return HttpResponseRedirect(reverse('order'))

@employee_required
@post_required
def placeOrder(request, menuID):
	employee = get_object_or_404(Employee, pk=request.session['employeeID'])
	menu = get_object_or_404(Menu, pk=menuID)
	order = Order(employee=employee, menu=menu)
	orderForm = OrderForm(request.POST, instance=order)

	if orderForm.is_valid():
		newOrder = orderForm.save()
		return HttpResponseRedirect(reverse('order'))
	else:
		return order(request, orderForm)

def menuList(request):
	if not request.user.is_authenticated() or not request.user.is_staff:
		return HttpResponseRedirect('/admin/') 
	return render_to_response('menu_list.html', {}, context_instance=RequestContext(request))

def orderList(request, menuID):
	if not request.user.is_authenticated() or not request.user.is_staff:
		return HttpResponseRedirect('/admin/')
	return render_to_response('order_list.html', { 'menuID': menuID }, context_instance=RequestContext(request))

