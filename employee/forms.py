from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError

from models import *

class LoginForm(forms.Form):
	username = forms.CharField(label='Username', error_messages={ 'required': 'Enter your username' })
	password = forms.CharField(label='Password', widget=forms.PasswordInput, error_messages={ 'required': 'Enter your password' })
	
	def ldap_check(self):
		ldap_result = { 'username': 'abrahamalrajhi@gmail.com', 'full_name': 'Ibrahim Al-Rajhi' }
		if not ldap_result: 
			self._errors['username'] = self.error_class(['Username and password don\'t match'])
		else:
			self.cleaned_data['full_name'] = ldap_result['full_name']

	def clean(self, *args, **kwargs):
		self.ldap_check()
		return super(LoginForm, self).clean(*args, **kwargs)


class EditEmployeeForm(ModelForm):
	class Meta:
		model = Employee
		exclude = ['full_name']

