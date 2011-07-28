from menu.models import MealForm, Meal, Menu, TimeSlot, Order
from employee.models import Employee

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib import auth

from datetime import date, datetime

def test(request):
    """docstring for test"""
    hello = "hello World"
    
    return render_to_response('hello.html',{'name':hello})

def createMeal(request):
    form = MealForm()
    return render_to_response('createMeal.html',{'form':form})

def createMenu():
    pass

def checkSpotsRemaining(timeSlotid, menuid):
    ordersForSlot = Order.objects.filter(menuid=menuid, timeslotid=timeSlotid);
    spotsAvail = int(TimeSlot.objects.get(pk=timeSlotid).capacity)
    return spotsAvail - len(ordersForSlot)

def makeAnOrder(post, menuid, request):
    mealid  = post['dinner']
    timeslotid = int(post['id_timeslot'])
    timeSlot = TimeSlot.objects.get(pk=timeslotid)
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

def cancelMeal(orders, meal_type):
    dinnerOrderIndex = findMeal(orders, meal_type)
    if dinnerOrderIndex != -1:
        orders[dinnerOrderIndex].delete()

        return HttpResponseRedirect(reverse('order'))

def confirmMeal(orders, meal_type):
    dinnerOrderIndex = findMeal(orders, meal_type)
    if dinnerOrderIndex != -1:
        dinnerOrder = orders[dinnerOrderIndex]
        dinnerOrder.state='c'
        dinnerOrder.confirm_time = datetime.today()
        dinnerOrder.save()

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
    
    if (len(orders) > 0):
        for order in orders:
            if order.state != 'x':
                if order.meal.meal_type == meal_type:
                    menuItem['orderStatus']=order.state
                    menuItem['regMeal']['meal'] = order.meal
                    menuItem['regMeal']['time'] = order.timeSlot.time
    
    if( not 'meal' in menuItem['regMeal']):
        menuItem['meals'] = menu.meals.filter(meal_type=meal_type)
   
    tSlots = TimeSlot.objects.filter(meal_type=meal_type)
    for timeSlot in tSlots:
        tSlot = {};
        tSlot['freespots'] = (checkSpotsRemaining(timeSlot.id, menu.id))
        #make the time look nicer
        tSlot['time'] = timeSlot.time
        tSlot['id'] = timeSlot.id
        tSlot['capacity'] = timeSlot.capacity
        menuItem['timeSlots'].append(tSlot)

    
    return menuItem
    

def order(request):
    #return render_to_response('order.html', {}, context_instanceext_instance=RequestContext(request))
    employee = Employee.objects.get(pk=request.session['employeeID'])
    orders = Order.objects.filter(employee=employee)
    regBreakfast = {}
    regLunch = {}
    regDinner = {}
    breakfasts = []
    lunches = []
    dinners = []
    orderStatus = {}
    error = []
    menuItems= []
    mess = ''

    # To handle the confirms nd cancel of the meals
    if '/menu/order/cancel' in request.path:
        cancelMeal(orders, request.path[-1])
        return HttpResponseRedirect(reverse('order'))

    if '/menu/order/confirm' in request.path:
        confirmMeal(orders, request.path[-1])

    if 'employeeID' not in request.session:
        return HttpResponseRedirect(reverse('login'))

    if ( Menu.objects.filter(startDate=date.today()).__str__() != [] ):
        menu = Menu.objects.filter(startDate=date.today().__str__())[0]
    else:
        menu=[];
        
    if request.method == 'POST' and request.POST != {}:
        mess=request.POST
        post=request.POST
        if  (('meal' and 'id_timeslot' and 'dinner') in post):
            makeAnOrder(post, menu.id, request)
            
        if (not 'dinner' in post):
            error.append('You forgot to pick a meal')

        if ('id_timeslot' in post):
            timeslotid = int(post['id_timeslot'])
            if( checkSpotsRemaining(timeslotid, menu.id) <1 ):
                error.append('That timeslot is full!')

    
    menuItems.append(createMenuItem(menu, orders, 'b'))
    menuItems.append(createMenuItem(menu, orders, 'l'))
    menuItems.append(createMenuItem(menu, orders, 'd'))

    #menu1 =  Menu.objects.create(description="yum lunch", expiration="2011-06-25", meal_type='b')
    return render_to_response('order.html',{'mess':mess, 'errors':error, 'menuItems':menuItems}, context_instance=RequestContext(request))
    
    
    
