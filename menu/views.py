# Create your views here.
from menu.models import MealForm, Meal

from django.http import HttpResponse
from django.shortcuts import render_to_response

def test(request):
    """docstring for test"""
    hello = "hello World"
    
    return render_to_response('hello.html',{'name':hello})

def createMeal(request):
    form = MealForm()
    return render_to_response('createMeal.html',{'form':form})

def createMenu():
    pass
    
