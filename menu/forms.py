from django import forms
from django.forms import ModelForm
from django.forms.widgets import RadioSelect, Select, Textarea
from django.core.exceptions import ValidationError

from models import *

class OrderForm(ModelForm):	
	meal = forms.ModelChoiceField(label='Meal Choices', widget=RadioSelect, queryset=None, empty_label=None)
	timeslot = forms.ModelChoiceField(label='Timeslots', widget=Select, queryset=None, empty_label=None)
	instructions = forms.CharField(label='Special Instructions', widget=Textarea, required=False)

	def __init__(self, target_menu, *args, **kwargs):
		super(OrderForm, self).__init__(*args, **kwargs)
		self.target_menu = target_menu
		self.fields['meal'].queryset = target_menu.meals
		self.fields['timeslot'].queryset = target_menu.timeslots
		self.fields['timeslot'].validators = [self.valid_timeslot]

		# gives each field a non '__unicode__' name (since it's dependant on the target_menu)
		choices = []
		for timeslot in self.fields['timeslot'].queryset.all():
			choices.append((timeslot.pk, timeslot.getFieldName(target_menu)))
		self.fields['timeslot'].choices = choices

		choices = []
		for meal in self.fields['meal'].queryset.all():
			choices.append((meal.pk, meal.getFieldName()))
		self.fields['meal'].choices = choices

	def valid_timeslot(self, timeslot):
		if not timeslot.isAvailableFor(self.target_menu):
			raise ValidationError('This timeslot is full and unavailable.')

	class Meta:
		model = Order
		fields = ['meal', 'timeslot', 'instructions']

