# Create your views here.

from django.shortcuts import render_to_response
from menu.models import Menu
from menu.models import Meal

def menuForToday(request):

    if request.method == 'GET' and request.GET != {}:
        mess=request.GET['dinner']
        mess = Meal.objects.get(pk=int(mess))
    else:
        mess = ''

    hello = "this is a test"
    menu = Menu.objects.all()[0]
    meals = menu.meals.all()

    breakfast = meals[0]
    lunch = meals[1]
    dinner1 = meals[2]
    dinner2 = meals[3]
    dinners = [dinner1, dinner2]


    #menu1 =  Menu.objects.create(description="yum lunch", expiration="2011-06-25", meal_type='b')
    return render_to_response('order.html',{'mess':mess, 'breakfast':breakfast, 'lunch':lunch, 'dinners':dinners})
    
    

