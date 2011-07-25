from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib import auth

from models import *

class LoginForm(forms.Form):
	username = forms.CharField(label='Username', error_messages={ 'required': 'Enter your username' })
	password = forms.CharField(label='Password', widget=forms.PasswordInput, error_messages={ 'required': 'Enter your password' })
	
<<<<<<< HEAD
	def ldap_check(self):
		ldap_result = { 'username': 'abraham' }
		if not ldap_result: 
			self._errors['username'] = self.error_class(['Username and password don\'t match'])
=======
	def authenticate_employee(self):
		# ldap_check would go here
		ldap_result = { 'username': 'abraham' }
		if !ldap_check: self._errors['username'] = self.error_class(['Username or password are incorrect.'])

		try:
			employee = Employee.objects.get(username=self.data['username'])
		except User.DoesNotExist:
			employee = Employee(username=

		user = auth.authenticate(username=self.data['username'], password=self.data['password'])
		if user is None:
			self._errors['username'] = self.error_class(['Username and password don\'t match.'])
		else: 
			if user.is_active == 'False':
				self._errors['username'] = self.error_class(['Account has been disabled.'])
>>>>>>> asjkd

	def clean(self, *args, **kwargs):
		self.ldap_check()
		return super(LoginForm, self).clean(*args, **kwargs)

class EditEmployeeForm(ModelForm):
	class Meta:                                                                                                                                                                                             
		model = Employee
