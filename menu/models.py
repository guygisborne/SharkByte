from datetime import date, time, datetime, timedelta

from django.db import models
from django.contrib.contenttypes import generic
from django.template.defaultfilters import date as date_filter

from employee.models import Employee

MENU_TYPES = (
	  ('b', 'breakfast')
	, ('l', 'lunch')
	, ('d', 'dinner')
)

ORDER_STATE = (
	  ('p', 'placed')
	, ('c', 'confirmed')
	, ('f', 'fulfilled')
)

CONFIRM_DELTA = 20

class Timeslot(models.Model):
	time = models.TimeField(help_text='Must be in <strong>HH:MM</strong> format; for example, 6:30 p.m. would be written as 18:30.')  
	capacity = models.PositiveIntegerField(blank=True, null=True, help_text='An optional limit of employees this timeslot can serve; leave blank to serve an unlimited number of employees.') 

	def availableCountFor(self, menu):
		from menu.models import Order 
		if self.capacity:
			used_slots = len(Order.objects.filter(menu=menu, timeslot=self))
			return self.capacity - used_slots
		else:
			return 0

	def isAvailableFor(self, menu):
		if self.capacity:
			return self.availableCountFor(menu) > 0
		else:
			return True

	def getFormattedTime(self):
		relative_time = datetime.combine(date.today(), self.time)
		return date_filter(relative_time, 'g:i a')

	def getFieldName(self, menu):
		if self.isAvailableFor(menu):
			if self.capacity:
				return '{0} ({1} available slots)'.format(self.getFormattedTime(), self.availableCountFor(menu))
			else:
				return '{0} (unlimited)'.format(self.getFormattedTime(), self.availableCountFor(menu))
		else:
			return '{0} (FULL)'.format(self.getFormattedTime())

	def __unicode__(self):
		if self.capacity:
			return u'{0} ({1} slot capacity)'.format(self.getFormattedTime(), self.capacity)
		else:
			return u'{0} (unlimited)'.format(self.time)


class Meal(models.Model):
	name = models.CharField(max_length=255)
	description = models.TextField()

	def __unicode__(self):
		return self.name

	def getFieldName(self, menu):
		return '{0} - {1}'.format(self.name, self.description)


class MenuManager(models.Manager):
	def todaysMenus(self, employee):
		todays_menus = []
		for type, typename in MENU_TYPES:
			menu = { 'typename': typename, 'menu': False, 'order': False }
			try:
				menu['menu'] = self.filter(type=type, publish_date=date.today())[0]
			except IndexError: 
				pass
			else:
				menu['order'] = menu['menu'].getOrderFor(employee)

			todays_menus.append(menu) 	
		return todays_menus

	def pastMenus(self, start_date=datetime.today(), count=15):
		days = []
		for i in xrange(count):
			cur_date = start_date - timedelta(days=i)
			name = date_filter(cur_date, 'F j, Y')
			menus = []
			for type, typename in MENU_TYPES:
				menu_info = {}
				try:
					menu = self.filter(type=type, publish_date=cur_date)[0]
				except IndexError:
					pass
				else:
					menu_info['menu'] = menu
					menu_info['placed_count'] = menu.getOrdersWithState('p', True)
					menu_info['confirmed_count'] = menu.getOrdersWithState('c', True) 
					menu_info['unfulfilled_count'] = menu_info['confirmed_count'] - menu.getOrdersWithState('f', True)
					menus.append(menu_info)

			days.append({ 'name': name, 'menus': menus })
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
		orders = Order.objects.filter(employee=employee, menu=self)
		return len(orders) > 0

	def getOrderFor(self, employee):
		from menu.models import Order
		if self.hasOrderFor(employee):
			return Order.objects.get(employee=employee, menu=self)
		else:
			return False

	def getOrdersWithState(self, state, count=False):
		orders = Order.objects.filter(menu=self, state=state)
		return (len(orders) if count else orders)

	def getAllOrders(self):
		orders = []
		for state, statename in ORDER_STATE:
			order = Order.objects.filter(menu=self, state=state).order_by('confirm_time')
			if len(order) > 0:
				orders.extend(order)
		return orders

	def isExpired(self):
		return self.end_time < datetime.time(datetime.now())

	def isPublishable(self):
		is_publishable = (self.publish_date == date.today())
		if self.publish_time:
			return is_publishable and self.publish_time < datetime.time(datetime.now())
		else:
			return is_publishable

	def __unicode__(self):
		return self.get_type_display()

	@models.permalink
	def getCreateURL(self):
		return ('create_order', (), { 'menu_id': self.pk })


class Order(models.Model):
	employee = models.ForeignKey(Employee)
	menu = models.ForeignKey(Menu)
	meal = models.ForeignKey(Meal)
	timeslot = models.ForeignKey(Timeslot)
	instructions = models.TextField(blank=True)
	state = models.CharField(max_length=1, choices=ORDER_STATE, default='p', editable=False) 
	confirm_time = models.DateTimeField(blank=True, null=True, editable=False)

	def getConfirmableTime(self):
		relative_time = datetime.combine(date.today(), self.timeslot.time)
		return relative_time - timedelta(minutes=CONFIRM_DELTA)

	def confirmableAt(self):
		return date_filter(self.getConfirmableTime(), 'g:i a')

	def isConfirmable(self):
		return self.getConfirmableTime() < datetime.now()

	def confirm(self):
		if self.isConfirmable():
			self.state = 'c'
			self.confirm_time = datetime.now()
			super(Order, self).save()

	def __unicode__(self):
		return '{0} ordered {1}'.format(self.employee, self.meal)

	@models.permalink
	def getConfirmURL(self):
		return ('confirm_order', (), { 'order_id': self.pk })

	@models.permalink
	def getCancelURL(self):
		return ('cancel_order', (), { 'order_id': self.pk })

