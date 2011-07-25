# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render_to_response

def test(request):
    """docstring for test"""
    hello = "hello World"
    
    return render_to_response('hello.html',{'name':hello})
