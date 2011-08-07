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
		self.overwrite_choice_names('meal')
		self.overwrite_choice_names('timeslot')

	def overwrite_choice_names(self, field_name):
		choices = []
		for field_model in self.fields[field_name].queryset.all():
			choices.append((field_model.pk, field_model.getFieldName(self.target_menu)))
		self.fields[field_name].choices = choices

	def valid_timeslot(self, timeslot):
		if not timeslot.isAvailableFor(self.target_menu):
			raise ValidationError('This timeslot is full and unavailable.')

	class Meta:
		model = Order
		fields = ['meal', 'timeslot', 'instructions']

