# Create your views here.
from datetime import date

from django.shortcuts import render_to_response
from django.template import RequestContext

from menu.models import Menu
from menu.models import Meal


def menuForToday(request):


    if request.method == 'POST' and request.POST != {}:
        mess=request.POST['dinner']
        mess = Meal.objects.get(pk=int(mess))
        
    else:
        mess = ''

    hello = "this is a test"
    menu = Menu.objects.filter(startDate=date.today().__str__())[0]

    breakfasts = menu.meals.filter(meal_type='b')
    lunches = menu.meals.filter(meal_type='l')
    dinners = menu.meals.filter(meal_type='d')




    #menu1 =  Menu.objects.create(description="yum lunch", expiration="2011-06-25", meal_type='b')
    return render_to_response('order.html',{'mess':mess, 'breakfasts':breakfasts, 'lunches':lunches, 'dinners':dinners}, context_instance=RequestContext(request))
    
