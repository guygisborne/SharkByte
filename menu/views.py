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

def order(request):
	if 'employeeID' not in request.session:
		return HttpResponseRedirect(reverse('login'))

	employee = get_object_or_404(Employee, pk=request.session['employeeID'])
	menus = Menu.managed.todaysMenus(employee)

	for menu in menus:
		menu['form'] = OrderForm(menu['menu'], instance=menu['menu']) if menu['menu'] else False

	return render_to_response('order.html', { 'menus': menus }, context_instance=RequestContext(request))

def cancelOrder(request, orderID):
    if 'employeeID' not in request.session:
        return HttpResponseRedirect(reverse('login'))

	employee = get_object_or_404(Employee, pk=request.session['employeeID'])
	order = get_object_or_404(Order, pk=orderID, employee=employee)
	order.delete()
	return HttpResponseRedirect(reverse('order'))

def confirmOrder(request, orderID):
    if 'employeeID' not in request.session:
        return HttpResponseRedirect(reverse('login'))

	employee = get_object_or_404(Employee, pk=request.session['employeeID'])
	order = get_object_or_404(Order, pk=orderID, employee=employee)

	if order.isConfirmable():
		order.confirm()
	return HttpResponseRedirect(reverse('order'))

def placeOrder(request, menuID):
	if 'employeeID' not in request.session:
		return HttpResponseRedirect(reverse('login'))

	if request.method != 'POST':
		return HttpResponseRedirect(reverse('order'))

	#employee = get_object_or_404(Employee, pk=request.session['employeeID'])
	#menu = get_object_or_404(Menu, pk=menuID)
	#meal = get_object_or_404(Meal, pk=formData['mealID'])
	#timeslot = get_object_or_404(Menu, pk=formData['timeslotID'])
	#instructions = formData['instructions']
	

def menuList(request):
	if not request.user.is_authenticated() or not request.user.is_staff:
		return HttpResponseRedirect('/admin/') 
	return render_to_response('menu_list.html', {}, context_instance=RequestContext(request))

def orderList(request, menuID):
	if not request.user.is_authenticated() or not request.user.is_staff:
		return HttpResponseRedirect('/admin/')
	return render_to_response('order_list.html', { 'menuID': menuID }, context_instance=RequestContext(request))

