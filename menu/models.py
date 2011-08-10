from datetime import date, time, datetime, timedelta

from django.db import models
from django.contrib.contenttypes import generic
from django.template.defaultfilters import date as date_filter
from django.template.defaultfilters import timeuntil

from employee.models import Employee

MENU_TYPES = (
	  ('b', 'breakfast')
	, ('l', 'lunch')
	, ('d', 'dinner')
)

ORDER_STATE = (
	  ('c', 'confirmed')
	, ('p', 'placed')
	, ('f', 'fulfilled')
)

CONFIRM_DELTA = 20

def relative_time(time):
	return datetime.combine(date.today(), time)

class Timeslot(models.Model):
	time = models.TimeField(help_text='Must be in <strong>HH:MM</strong> format; for example, 6:30 p.m. would be written as 18:30.')  
	capacity = models.PositiveIntegerField(blank=True, null=True, help_text='An optional limit of employees this timeslot can serve; leave blank to serve an unlimited number of employees.') 

	def availableCountFor(self, menu):
		from menu.models import Order 
		if self.capacity != None:
			used_slots = len(Order.objects.filter(menu=menu, timeslot=self))
			return self.capacity - used_slots

	def isAvailableFor(self, menu):
		return (self.availableCountFor(menu) > 0 if self.capacity != None else True)

	def getFormattedTime(self):
		return date_filter(relative_time(self.time), 'g:i a')

	def getFieldName(self, menu):
		field_name = self.getFormattedTime()
		if self.isAvailableFor(menu):
			if self.capacity != None:
				field_name = '{0} ({1} available slots)'.format(field_name, self.availableCountFor(menu))
			else:
				field_name = '{0} (unlimited)'.format(field_name)
		else:
			field_name = '{0} (FULL)'.format(field_name)
		return field_name

	def __unicode__(self):
		if self.capacity != None:
			return u'{0} ({1} slot capacity)'.format(self.getFormattedTime(), self.capacity)
		else:
			return u'{0} (unlimited)'.format(self.getFormattedTime())


class Meal(models.Model):
	name = models.CharField(max_length=255)
	description = models.TextField()

	def getFieldName(self, menu=None):
		return '{0} - {1}'.format(self.name, self.description)

	def __unicode__(self):
		return self.name


def tryGetMenu(type, publish_date):
	try:
		menu = Menu.objects.filter(type=type, publish_date=publish_date)[0]
	except IndexError:
		return False
	else:
		return menu

class MenuManager(models.Manager):
	def todaysMenus(self, employee):
		todays_menus = []
		for type, typename in MENU_TYPES:
			menu = tryGetMenu(type, date.today())
			order = (menu.getOrderFor(employee) if menu else False)
			todays_menus.append({ 'typename': typename.capitalize(), 'menu': menu, 'order': order }) 	
		return todays_menus

	def pastMenus(self, start_date=datetime.today(), count=15):
		days = []
		for i in xrange(count):
			curdate = start_date - timedelta(days=i)
			datename = date_filter(curdate, 'F j, Y')
			empty = True
			menus = []

			for type, typename in MENU_TYPES:
				menu = tryGetMenu(type, curdate)
				if menu:
					empty = False
					unfulfilled_count = menu.getOrdersWithState('c')
					confirmed_count = menu.getOrdersWithState('f') + unfulfilled_count
					placed_count = menu.getOrdersWithState('p') + confirmed_count
					menus.append({
						  'menu': menu
						, 'placed_count': placed_count
						, 'confirmed_count': confirmed_count
						, 'unfulfilled_count': unfulfilled_count
					})
			days.append({ 'datename': datename, 'menus': menus, 'empty': empty })
		return days


class Menu(models.Model):
	type = models.CharField(max_length=1, choices=MENU_TYPES)
	meals = models.ManyToManyField(Meal)
	timeslots = models.ManyToManyField(Timeslot)
	description = models.TextField(blank=True);
	publish_date = models.DateField(help_text='The day this menu will be available.')
	publish_time = models.TimeField(blank=True, null=True, help_text='An optional time when this menu will be available at. Must be in <strong>HH:MM</strong> format; for example, 6:30 p.m. would be written as 18:30.')
	end_time = models.TimeField(help_text='The time when this menu will expire and become unavailable. Must be in <strong>HH:MM</strong> format; for example, 6:30 p.m. would be written as 18:30.')

	objects = models.Manager()
	managed = MenuManager()

	def hasTimeslot(self, timeslot):
		timeslots = self.timeslots.filter(pk=timeslot.pk)
		return len(timeslots) > 0

	def hasMeal(self, meal):
		meals = self.meals.filter(pk=meal.pk)
		return len(meals) > 0

	def hasOrderFor(self, employee):
		from menu.models import Order
		orders = Order.objects.filter(menu=self, employee=employee)
		return len(orders) > 0

	def getOrderFor(self, employee):
		from menu.models import Order
		if self.hasOrderFor(employee):
			return Order.objects.get(menu=self, employee=employee)
		else:
			return False

	def getOrdersWithState(self, state, count=True):
		orders = Order.objects.filter(menu=self, state=state).order_by('confirm_time')
		return (len(orders) if count else orders)

	def getAllOrders(self):
		orders = []
		for state, statename in ORDER_STATE:
			order = self.getOrdersWithState(state, False)
			if len(order) > 0:
				orders.extend(order)
		return orders

	def getTimeuntilEnd(self):
		return timeuntil(datetime.combine(date.today(), self.end_time))

	def endTimeString(self):
		return date_filter(relative_time(self.end_time), 'g:i a')

	def isExpired(self):
		return self.end_time < datetime.time(datetime.now())

	def isPublishable(self):
		publishable_today = (self.publish_date == date.today())
		if self.publish_time:
			return publishable_today and self.publish_time < datetime.time(datetime.now())
		else:
			return publishable_today

	def __unicode__(self):
		return self.get_type_display()


class Order(models.Model):
	employee = models.ForeignKey(Employee)
	menu = models.ForeignKey(Menu)
	meal = models.ForeignKey(Meal)
	timeslot = models.ForeignKey(Timeslot)
	instructions = models.TextField(blank=True)
	state = models.CharField(max_length=1, choices=ORDER_STATE, default='p', editable=False) 
	confirm_time = models.DateTimeField(blank=True, null=True, editable=False)

	def getConfirmableTime(self):
		return relative_time(self.timeslot.time) - timedelta(minutes=CONFIRM_DELTA)

	def confirmableTimeString(self):
		return date_filter(self.getConfirmableTime(), 'g:i a')

	def isConfirmable(self):
		return self.getConfirmableTime() < datetime.now()

	def confirm(self):
		if self.isConfirmable():
			self.state = 'c'
			self.confirm_time = datetime.now()
			super(Order, self).save()
			return True
		return False

	def __unicode__(self):
		return '{0} ordered {1}'.format(self.employee, self.meal)


