from menu.models import MealForm, Meal, Menu, TimeSlot

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

def order(request):
    #return render_to_response('order.html', {}, context_instanceext_instance=RequestContext(request))

    if request.method == 'POST' and request.POST != {}:
        mess=request.POST
        
    else:
        mess = ''


    hello = "this is a test"
    if( Menu.objects.filter(startDate=date.today().__str__()) != []):
        menu = Menu.objects.filter(startDate=date.today().__str__())[0]
    else:
        menu=[];

    timeSlots = TimeSlot.objects.all()
    breakfasts = menu.meals.filter(meal_type='b')
    lunches = menu.meals.filter(meal_type='l')
    dinners = menu.meals.filter(meal_type='d')

    

    #menu1 =  Menu.objects.create(description="yum lunch", expiration="2011-06-25", meal_type='b')
    return render_to_response('order.html',{'mess':mess, 'breakfasts':breakfasts, 'lunches':lunches, 'dinners':dinners, 'timeSlots':timeSlots}, context_instance=RequestContext(request))
    

