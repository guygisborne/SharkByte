from datetime import date, time, datetime, timedelta

from django.db import models
from django.contrib.contenttypes import generic

from employee.models import Employee

MENU_TYPES = (
	  ('b', 'breakfast')
	, ('l', 'lunch')
	, ('d', 'dinner')
)

CONFIRM_MIN_DELTA = 20

class Timeslot(models.Model):
	time = models.TimeField(help_text='Must be in <strong>HH:MM</strong> format; for example, 6:30 p.m. would be written as 18:30.')  
	capacity = models.PositiveIntegerField(blank=True, null=True, help_text='An optional limit of employees this timeslot can serve; leave blank to serve an unlimited number of employees.') 

	def availableCountFor(self, menu):
		from menu.models import Order 
		used_slots = len(Order.objects.filter(menu=menu, timeslot=self))
		return self.capacity - used_slots

	def isAvailableFor(self, menu):
		if self.capacity:
			return self.availableCountFor(menu) > 0
		else:
			return True

	def __unicode__(self):
		if self.capacity:
			return u'{0} ({1} slot capacity)'.format(self.time, self.capacity)
		else:
			return u'{0}'.format(self.time)

	def getFieldName(self, menu):
		formatted_time = self.time.strftime('%I:%M %p')
		return '{0} ({1} available slots)'.format(formatted_time, self.availableCountFor(menu))


class Meal(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __unicode__(self):
        return self.name


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


class Menu(models.Model):
	type = models.CharField(max_length=1, choices=MENU_TYPES)
	meals = models.ManyToManyField(Meal)
	timeslots = models.ManyToManyField(Timeslot)
	description = models.TextField(blank=True);
	publish_date = models.DateField(help_text='The day this menu will be available for.')
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
	is_confirmed = models.BooleanField(default=False, editable=False) 
	confirmed_at = models.DateTimeField(blank=True, null=True, editable=False)

	def confirmableAt(self):
		return self.timeslot.time - timedelta(minutes=20)

	def isConfirmable(self):
		return self.confirmable_at < datetime.time(datetime.now())

	def confirm(self):
		self.is_confirmed = True
		self.confirmed_at = datetime.now()
		super(Order, self).save()

	def __unicode__(self):
		return '{0} ordered {1}'.format(self.employee, self.meal)

	@models.permalink
	def getConfirmURL(self):
		return ('confirm_order', (), { 'order_id': self.pk })

	@models.permalink
	def getCancelURL(self):
		return ('cancel_order', (), { 'order_id': self.pk })

