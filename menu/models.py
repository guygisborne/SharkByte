from datetime import datetime

from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.forms import ModelForm
from django.utils.encoding import smart_str

from employee.models import Employee

MEAL_TYPES = (
	('b', 'breakfast'),
	('l', 'lunch'),
	('d', 'dinner'),
)

ORDER_STATE = (
	('r', 'register'),
	('c', 'confirmed'),
	('x', 'canceled'),
	('n', 'noshow'),
)

class TimeSlot(models.Model):
    time = models.CharField(max_length=6, help_text="Time must be formatted as HH:MM")  
    capacity = models.CharField(max_length=4, help_text="How many people can sign up for this time slot")
    
    def __str__(self):
        return smart_str('%s - %s' % (self.time, self.capacity))

class Meal(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    meal_type = models.CharField(max_length=1, choices=MEAL_TYPES)

    pub_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return smart_str('%s - %s' % (self.name, self.meal_type))


class MealForm(ModelForm):
    class Meta:
        model = Meal


class Menu(models.Model):
    description = models.TextField(blank=True);
    meals = models.ManyToManyField(Meal, through="MealToMenu")
    timeSlot = models.ManyToManyField(TimeSlot, through="MealToMenu")
    startDate = models.DateField(help_text="Dates must be formatted as YYYY-MM-DD HH:MM:SS, so 'June 25, 2011 Midnight' is '2011-06-25'")
    expiration = models.DateField(help_text="Dates must be formatted as YYYY-MM-DD HH:MM:SS, so 'June 25, 2011 Midnight' is '2011-06-25'")

    def __str__(self):
        return smart_str('%s' % (self.description))

class MealToMenu(models.Model):
    meal = models.ForeignKey(Meal)
    timeSlot = models.ForeignKey(TimeSlot)
    menu = models.ForeignKey(Menu)

    def __str__(self):
        return smart_str('%s - %s' % (self.meal, self.timeSlot))

class Order(models.Model):
    employee = models.ForeignKey(Employee)
    timeSlot = models.ForeignKey(TimeSlot)
    #menu = models.ForeignKey(Menu)
    meal = models.ForeignKey(Meal)
    instructions = models.TextField(blank=True, help_text="Something Here")
    state = models.CharField(max_length=1, choices=ORDER_STATE) # confirm, cancel, complete, submitted
    pub_date = models.DateTimeField(auto_now_add=True)

    def save(self):
        # make sure the meal hasn't expired on submission
        # make sure there isn't already an order placed by this employee on this menu
        super(Order, self).save()

    def __unicode__(self):
        return '{0} ordered {1}'.format(self.employee, self.meal)

#class OrderForm(forms.Form)
    #pass

    
