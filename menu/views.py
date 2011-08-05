from datetime import date, datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib import auth

from forms import *
from models import *
from decorators import *
from employee.models import *

@employee_required
def order_list(request, prev_form=None, **kwargs):
	menus = Menu.managed.todaysMenus(kwargs['employee'])
	for menu in menus:
		if menu['menu']:
			if prev_form and prev_form.target_menu == menu['menu']:
				menu['form'] = prev_form
			else:
				menu['form'] = OrderForm(menu['menu'])
		else:
			menu['form'] = False
	return render_to_response('order_list.html', { 'menus': menus }, context_instance=RequestContext(request))

@employee_required
@post_required('/menu/order-list/')
def create_order(request, menu_id, **kwargs):
	menu = get_object_or_404(Menu, pk=menu_id)
	new_order = Order(employee=kwargs['employee'], menu=menu)
	order_form = OrderForm(menu, request.POST, instance=new_order)
	if order_form.is_valid():
		new_order = order_form.save()
		return HttpResponseRedirect(reverse('order_list'))
	else:
		return order_list(request, order_form)

@employee_required
def confirm_order(request, order_id, **kwargs):
	order = get_object_or_404(Order, pk=order_id, employee=kwargs['employee'])
	if order.isConfirmable():
		order.confirm()
	return HttpResponseRedirect(reverse('order_list'))

@employee_required
def cancel_order(request, order_id, **kwargs):
	order = get_object_or_404(Order, pk=order_id, employee=kwargs['employee'])
	order.delete()
	return HttpResponseRedirect(reverse('order_list'))

@staff_required
def menu_list(request):
	return render_to_response('menu_list.html', {}, context_instance=RequestContext(request))

@staff_required
def orders_list(request, menu_id):
	return render_to_response('order_list.html', { 'menu_id': menu_id }, context_instance=RequestContext(request))

