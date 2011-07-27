from menu.models import MealForm, Meal

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib import auth




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
    return render_to_response('order.html', {}, context_instanceext_instance=RequestContext(request))
