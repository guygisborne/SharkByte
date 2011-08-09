from datetime import date, datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib import auth
from django.utils import simplejson

from decorators import *
from forms import *
from models import *
from employee.models import *

@employee_required
def todays_menu(request, prev_form=None, **kwargs):
	menus = Menu.managed.todaysMenus(kwargs['employee'])
	for menu in menus:
		if menu['menu']:
			if prev_form and prev_form.target_menu == menu['menu']:
				menu['form'] = prev_form
			else:
				menu['form'] = OrderForm(menu['menu'])
		else:
			menu['form'] = False
	return render_to_response('todays_menu.html', { 'menus': menus }, context_instance=RequestContext(request))

@employee_required
@post_required('todays_menu')
def create_order(request, menu_id, **kwargs):
	menu = get_object_or_404(Menu, pk=menu_id)
	new_order = Order(employee=kwargs['employee'], menu=menu)
	order_form = OrderForm(menu, request.POST, instance=new_order)
	if order_form.is_valid():
		order_form.save()
		return HttpResponseRedirect(reverse('todays_menu'))
	else:
		return todays_menu(request, order_form)

@employee_required
def confirm_order(request, order_id, **kwargs):
	order = get_object_or_404(Order, pk=order_id, employee=kwargs['employee'])
	if order.isConfirmable():
		order.confirm()
	return HttpResponseRedirect(reverse('todays_menu'))

@employee_required
def cancel_order(request, order_id, **kwargs):
	order = get_object_or_404(Order, pk=order_id, employee=kwargs['employee'])
	order.delete()
	return HttpResponseRedirect(reverse('todays_menu'))

@staff_required
def menu_list(request):
	days = Menu.managed.pastMenus()
	return render_to_response('menu_list.html', { 'days': days }, context_instance=RequestContext(request))

@staff_required
def order_list(request, menu_id):
	menu = get_object_or_404(Menu, pk=menu_id)
	return render_to_response('order_list.html', { 'menu': menu }, context_instance=RequestContext(request))

@staff_required
def get_orders(request, menu_id):
	menu = get_object_or_404(Menu, pk=menu_id)
	orders = menu.getAllOrders()
	response = [json_order(order) for order in orders]
	return HttpResponse(simplejson.dumps(response), mimetype='application/javascript')

def json_order(order):
	return {
		  'pk': order.pk
		, 'name': order.employee.__unicode__()
		, 'state': order.get_state_display()
		, 'timeslot': order.timeslot.getFormattedTime()
		, 'meal': order.meal.__unicode__()
		, 'instructions': order.instructions
		, 'allergies': order.employee.allergies
		, 'diet': order.employee.diet
	}

@staff_required
@post_required('menu_list')
def fulfill_orders(request, menu_id):
	order_ids = simplejson.loads(request.POST['order_ids'])
	orders = [order_from_id(order_id) for order_id in order_ids]
	response = [change_order_state(order) if order else False for order in orders]
	return HttpResponse(simplejson.dumps(response), mimetype='application/javascript')

def order_from_id(order_id):
	try:
		return Order.objects.get(pk=order_id)
	except DoesNotExist:
		return False
	
def change_order_state(order):
	order.state = 'f'
	order.save()
	return order.pk

