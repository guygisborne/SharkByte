# Create your views here.
from datetime import date

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect

from django.core.urlresolvers import reverse


from menu.models import Menu
from menu.models import Meal
from forms import *
from models import *

def login(request, prev_login_form=None):
	if 'employeeID' in request.session:
		return HttpResponseRedirect(reverse('order'))

	login_form = (prev_login_form if prev_login_form else LoginForm())
	return render_to_response('login.html', { 'login_form': login_form }, context_instance=RequestContext(request))

def authenticate(request):
	if request.method != 'POST':
		return HttpResponseRedirect(reverse('login'))

	login_form = LoginForm(request.POST)
	if not login_form.is_valid():
		return login(request, login_form)

	employee = Employee.objects.get_or_create(username=login_form.cleaned_data['username'], defaults={ 'display_name': login_form.cleaned_data['display_name'] })
	employee = { 'employeeID': employee[0].pk, 'is_new': employee[1] }
	request.session['employeeID'] = employee['employeeID']

	if employee['is_new']:
		return HttpResponseRedirect(reverse('edit-profile'))
	else:
		return HttpResponseRedirect(reverse('order'))

def logout(request):
	if 'employeeID' in request.session:
		del request.session['employeeID']

	return HttpResponseRedirect(reverse('login'))

def editProfile(request):
	if 'employeeID' not in request.session:
		return HttpResponseRedirect(reverse('login'))

	employee = get_object_or_404(Employee, pk=request.session['employeeID'])
	success = False
	if request.method == 'POST':
		employee_form = EditEmployeeForm(request.POST, instance=employee)
		if employee_form.is_valid():
			employee_form.save()
			success = True
	else:
		employee_form = EditEmployeeForm(instance=employee)

	return render_to_response('edit_profile.html', { 'employee_form': employee_form, 'success': success }, context_instance=RequestContext(request))


def menuForToday(request):

    if request.method == 'POST' and request.POST != {}:
        mess=request.POST['dinner']
        mess = Meal.objects.get(pk=int(mess))
        
    else:
        mess = ''

    mess = request.session['employeeID']

    hello = "this is a test"
    menu = Menu.objects.filter(startDate=date.today().__str__())[0]

    breakfasts = menu.meals.filter(meal_type='b')
    lunches = menu.meals.filter(meal_type='l')
    dinners = menu.meals.filter(meal_type='d')

    

    #menu1 =  Menu.objects.create(description="yum lunch", expiration="2011-06-25", meal_type='b')
    return render_to_response('order.html',{'mess':mess, 'breakfasts':breakfasts, 'lunches':lunches, 'dinners':dinners}, context_instance=RequestContext(request))
    

