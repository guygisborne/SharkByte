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

	formData = request['POST']
	employee = get_object_or_404(Employee, pk=request.session['employeeID'])
	menu = get_object_or_404(Menu, pk=menuID)

	# is there already an order for this employee for this menu?
	# is the timeslot available?
	# was a meal selected?

	order = Order(
		employee = get_object_or_404(Employee, pk=request.session['employeeID']),
		menu = get_object_or_404(Menu, pk=formData['menuID']),
		timeslot = get_object_or_404(Timeslot, pk=formData['timeslotID']),
		meal = meal,
		instructions = formData['instructions'],
		state = 'r'
	)



def menuList(request):
	if not request.user.is_authenticated() or not request.user.is_staff:
		return HttpResponseRedirect('/admin/') 

	return render_to_response('menu_list.html', {}, context_instance=RequestContext(request))

def orderList(request, menuID):
	if not request.user.is_authenticated() or not request.user.is_staff:
		return HttpResponseRedirect('/admin/')

	return render_to_response('order_list.html', { 'menuID': menuID }, context_instance=RequestContext(request))


# DANGER ZONE

def makeAnOrder(post, menuid, request):
    mealid  = post['dinner']
    timeslotid = int(post['id_timeslot'])
    timeSlot = Timeslot.objects.get(pk=timeslotid)
    employee = Employee.objects.get(pk=request.session['employeeID'])
    meal = Meal.objects.get(pk=mealid)
    instructions = post['specialIns']
    state = 'r'

    orders = Order.objects.filter(employee=employee)
    if (findMeal(orders, meal.meal_type) == -1):
        if( checkSpotsRemaining(timeslotid, menuid) > 0):
            newOrder = Order(employee=employee, timeSlot=timeSlot, menuid=menuid, timeslotid=timeslotid, meal=meal, instructions=instructions, state=state)

            newOrder.save()

def returnMeals(orders, state):
    registeredMeals= []

    for order in orders:
        meal={}
        if order.state==state:
            meal['name'] = order.meal.name
            meal['type'] = order.meal.meal_type
            meal['description'] = order.meal.description
            meal['time'] = order.timeSlot.time
            registeredMeals.append(meal)

    return registeredMeals
           

def findMeal(orders, meal_type):
    """docstring for findMeal"""
    for i in range(len(orders)):
        if orders[i].meal.meal_type == meal_type:
            return i
    return -1

# do this in the Menu Model
def createMenuItem(menu, orders, meal_type):
    """This Function retruns a menu item dictionary for the corresponding menu"""
    menuItem = {}
    menuItem['regMeal'] = {}
    menuItem['meals'] = []
    menuItem['timeSlots'] = []
    
    if meal_type == 'b':
        menuItem['formalName']='Breakfast'
    if meal_type == 'l':
        menuItem['formalName']='Lunch'
    if meal_type == 'd':
        menuItem['formalName']='Dinner'
    
	# filter in the Order Model
    if (len(orders) > 0):
        for order in orders:
            if order.state != 'x':
                if order.meal.meal_type == meal_type:
                    menuItem['orderStatus']=order.state
                    menuItem['regMeal']['meal'] = order.meal
                    menuItem['regMeal']['time'] = order.timeSlot.time
                    menuItem['timeWindow'] = checkConfirmTimeWindow(order.timeSlot.time)
    
    if( not 'meal' in menuItem['regMeal']):
        menuItem['meals'] = menu.meals.filter(meal_type=meal_type)
   
    tSlots = Timeslot.objects.filter(meal_type=meal_type)
    for timeSlot in tSlots:
        tSlot = {};
        tSlot['freespots'] = (checkSpotsRemaining(timeSlot.id, menu.id))
        #make the time look nicer
        tSlot['time'] = timeSlot.time
        tSlot['id'] = timeSlot.id
        tSlot['capacity'] = timeSlot.capacity
        menuItem['timeSlots'].append(tSlot)

    
    return menuItem
    
def checkConfirmTimeWindow(time):
    timeWindow = 20
    currentTime = datetime.datetime.today() + datetime.timedelta(hours=1, minutes=timeWindow)
    return ( currentTime.time() > time )
