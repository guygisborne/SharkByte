from django import forms
from django.forms import ModelForm
from django.forms.widgets import RadioSelect, Select

from models import *

class OrderForm(ModelForm):	
	meal = forms.ModelChoiceField(widget=RadioSelect, queryset=None, empty_label=None)
	timeslot = forms.ModelChoiceField(widget=Select, queryset=None, empty_label=None)

	def __init__(self, targetMenu, *args, **kwargs):
		super(OrderForm, self).__init__(*args, **kwargs)
		self.fields['meal'].queryset = targetMenu.meals
		self.fields['timeslot'].queryset = targetMenu.timeslots

		# todo: make this nicer?
		choices = []
		for timeslot in self.fields['timeslot'].queryset.all():
			choices.append((timeslot.pk, '{0} - 12 available slots'.format(timeslot.time)))
		self.fields['timeslot'].choices = choices

	class Meta:
		model = Order
		fields = ['meal', 'timeslot', 'instructions']
