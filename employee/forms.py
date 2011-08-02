from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib import auth

from models import *

class LoginForm(forms.Form):
	username = forms.CharField(label='Username', error_messages={ 'required': 'Enter your username' })
	password = forms.CharField(label='Password', widget=forms.PasswordInput, error_messages={ 'required': 'Enter your password' })
	
	def ldap_check(self):
		ldap_result = { 'username': 'Abraham Al-Rajhi' }
		if not ldap_result: 
			self._errors['username'] = self.error_class(['Username and password don\'t match'])

		self.cleaned_data['display_name'] = ldap_result['username']

	def clean(self, *args, **kwargs):
		self.ldap_check()
		return super(LoginForm, self).clean(*args, **kwargs)


class EditEmployeeForm(ModelForm):
	class Meta:
		model = Employee
