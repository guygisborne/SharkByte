from functools import wraps

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse

from employee.models import *

def employee_required(view_fn):
	def decorated(request, *args, **kwargs):
		if 'employee_id' not in request.session:
			return HttpResponseRedirect(reverse('login'))
		else:
			kwargs['employee'] = get_object_or_404(Employee, pk=request.session['employee_id'])
			return view_fn(request, *args, **kwargs)

	return decorated

def post_required(url_name):
	def decorator(view_fn):
		def decorated(request, *args, **kwargs):
			if request.method != 'POST':
				return HttpResponseRedirect(reverse(url_name))
			else:
				return view_fn(request, *args, **kwargs)

		return wraps(view_fn)(decorated)
	
	return decorator

def staff_required(view_fn):
	def decorated(request, *args, **kwargs):
		if not request.user.is_authenticated() or not request.user.is_staff:
			return HttpResponseRedirect(reverse('admin:index'))
		else:
			return view_fn(request, *args, **kwargs)

	return decorated

