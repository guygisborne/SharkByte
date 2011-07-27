from datetime import datetime

from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.forms import ModelForm

from employee.models import Employee

MEAL_TYPES = (
	('b', 'breakfast'),
	('l', 'lunch'),
	('d', 'dinner'),
)

class Meal(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    meal_type = models.CharField(max_length=1, choices=MEAL_TYPES)

    pub_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

class MealForm(ModelForm):
    class Meta:
        model = Meal


class Menu(models.Model):
	description = models.TextField(blank=True);
	meal_type = models.CharField(max_length=1, choices=MEAL_TYPES)
	meals = models.ManyToManyField(Meal, through="MealToMenu")
	expiration = models.DateTimeField(help_text="Dates must be formatted as YYYY-MM-DD HH:MM:SS, so 'June 25, 2011 Midnight' is '2011-06-25 24:00:00'")


class MealToMenu(models.Model):
    meal = models.ForeignKey(Meal)
    menu = models.ForeignKey(Menu)


class Order(models.Model):
	employee = models.ForeignKey(Employee)
	menu = models.ForeignKey(Menu)
	meal = models.ForeignKey(Meal)
	instructions = models.TextField(blank=True, help_text="Something Here")
	#state = # confirm, cancel, complete, submitted

	pub_date = models.DateTimeField(auto_now_add=True)

	def save(self):
		# make sure the meal hasn't expired on submission
		# make sure there isn't already an order placed by this employee on this menu
		super(Order, self).save()

	def __unicode__(self):
		return '{0} ordered {1}'.format(self.employee, self.meal)


    
