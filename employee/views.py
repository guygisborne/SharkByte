from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from menu.decorators import *
from forms import *
from models import *

def login(request, prev_login_form=None):
	if 'employee_id' in request.session:
		return HttpResponseRedirect(reverse('order_list'))
	else:
		login_form = (prev_login_form if prev_login_form else LoginForm())
		return render_to_response('login.html', { 'login_form': login_form }, context_instance=RequestContext(request))

@employee_required
def logout(request, **kwargs):
	del request.session['employee_id']
	return HttpResponseRedirect(reverse('login'))

@post_required('login')
def authenticate(request):
	login_form = LoginForm(request.POST)
	if not login_form.is_valid():
		return login(request, login_form)
	else:
		employee = Employee.objects.get_or_create(username=login_form.cleaned_data['username'], defaults={ 'full_name': login_form.cleaned_data['full_name'] })
		result = { 'employee_id': employee[0].pk, 'is_new': employee[1] }
		request.session['employee_id'] = result['employee_id']
		redirect_url = (reverse('edit_profile') if result['is_new'] else reverse('order_list'))
		return HttpResponseRedirect(redirect_url)

@employee_required
def edit_profile(request, **kwargs):
	success = False
	if request.method == 'POST':
		employee_form = EditEmployeeForm(request.POST, instance=kwargs['employee'])
		if employee_form.is_valid():
			employee_form.save()
			success = True
	else:
		employee_form = EditEmployeeForm(instance=kwargs['employee'])

	return render_to_response('edit_profile.html', { 'employee_form': employee_form, 'success': success }, context_instance=RequestContext(request))

