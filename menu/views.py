from menu.models import MealForm, Meal, Menu, TimeSlot, Order

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib import auth

from datetime import date

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

def order(request):
    #return render_to_response('order.html', {}, context_instanceext_instance=RequestContext(request))

    if( Menu.objects.filter(startDate=date.today().__str__()) != []):
        menu = Menu.objects.filter(startDate=date.today().__str__())[0]
    else:
        menu=[];
        
    if request.method == 'POST' and request.POST != {}:
        mess=request.POST
        post=request.POST
        timeslotid = post['TimeSlots']

        
    else:
        mess = ''



    timeSlots = TimeSlot.objects.all()
    freeSpots = [];

    for timeSlot in timeSlots:
        freeSpots.append(checkSpotsRemaining(timeSlot.id, menu.id))

    breakfasts = menu.meals.filter(meal_type='b')
    lunches = menu.meals.filter(meal_type='l')
    dinners = menu.meals.filter(meal_type='d')

    

    #menu1 =  Menu.objects.create(description="yum lunch", expiration="2011-06-25", meal_type='b')
    return render_to_response('order.html',{'mess':mess, 'breakfasts':breakfasts, 'lunches':lunches, 'dinners':dinners, 'timeSlots':timeSlots, 'freeSpots':freeSpots}, context_instance=RequestContext(request))
    
    
    
