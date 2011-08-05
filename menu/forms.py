from django import forms
from django.forms import ModelForm
from django.forms.widgets import RadioSelect, Select, Textarea

from models import *

class OrderForm(ModelForm):	
	meal = forms.ModelChoiceField(label='Meal Choices', widget=RadioSelect, queryset=None, empty_label=None)
	timeslot = forms.ModelChoiceField(label='Timeslots', widget=Select, queryset=None, empty_label=None)
	instructions = forms.CharField(label='Special Instructions', widget=Textarea)

	def __init__(self, target_menu, *args, **kwargs):
		super(OrderForm, self).__init__(*args, **kwargs)
		self.fields['meal'].queryset = target_menu.meals
		self.fields['timeslot'].queryset = target_menu.timeslots

		# gives each timeslot a non '__unicode__' name (since it's dependant on the target_menu)
		choices = []
		for timeslot in self.fields['timeslot'].queryset.all():
			choices.append((timeslot.pk, timeslot.getFieldName(target_menu)))
		self.fields['timeslot'].choices = choices

	class Meta:
		model = Order
		fields = ['meal', 'timeslot', 'instructions']

