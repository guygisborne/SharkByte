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
	capacity = models.PositiveIntegerField(help_text='Number of employees this timeslot can serve.') 

	def availableCountFor(menu, self):
		from menu.models import Order 
		usedSlots = len(Order.objects.filter(menu=menu, timeslot=self))
		return self.capacity - usedSlots

	def isAvailableFor(menu, self):
		return self.availableCountFor(menu) > 0

	def __unicode__(self):
		return u'{0} ({1} slot capacity)'.format(self.time, self.capacity)


class Meal(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __unicode__(self):
        return self.name


class MenuManager(models.Manager):
	def todaysMenus(self, employee):
		todaysMenus = []

		for type, typeName in MENU_TYPES:
			menu = False
			order = False

			try:
				menu = self.filter(type=type, publishDate=date.today())[0]
			except IndexError: 
				pass
			else:
				order = menu.getOrderFor(employee)

			todaysMenus.append((typeName, menu, order)) 	

		print todaysMenus
		return todaysMenus


class Menu(models.Model):
	type = models.CharField(max_length=1, choices=MENU_TYPES)
	meals = models.ManyToManyField(Meal)
	timeslots = models.ManyToManyField(Timeslot)
	description = models.TextField(blank=True);
	publishDate = models.DateField(help_text='The day this menu will be available for.')
	publishTime = models.TimeField(blank=True, help_text='An optional time when this menu will be available at. Must be in <strong>HH:MM</strong> format; for example, 6:30 p.m. would be written as 18:30.')
	endTime = models.TimeField(help_text='The time when this menu will expire and become unavailable. Must be in <strong>HH:MM</strong> format; for example, 6:30 p.m. would be written as 18:30.')

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
		return self.endTime < datetime.time(datetime.now())

	def isPublishable(self):
		isPublishable = (self.publishDate == date.today())
		if self.publishTime:
			return isPublishable and self.publishTime < datetime.time(datetime.now())
		else:
			return isPublishable

	def __unicode__(self):
		return self.get_type_display()

	@models.permalink
	def getPlaceURL(self):
		return ('place', (), { 'menuID': self.pk })

class Order(models.Model):
	employee = models.ForeignKey(Employee)
	menu = models.ForeignKey(Menu)
	meal = models.ForeignKey(Meal)
	timeslot = models.ForeignKey(Timeslot)
	instructions = models.TextField(blank=True)
	isConfirmed = models.BooleanField(default=False) 
	confirmedAt = models.DateTimeField(blank=True, null=True)

	def confirmableAt(self):
		return self.timeslot.time - timedelta(minutes=CONFIRM_MIN_DELTA)

	def isConfirmable(self):
		return self.confirmableAt < datetime.time(datetime.now())

	def confirm(self):
		self.isConfirmed = True
		self.confirmedAt = datetime.now()
		super(Order, self).save()

	def __unicode__(self):
		return '{0} ordered {1}'.format(self.employee, self.meal)

	@models.permalink
	def getConfirmURL(self):
		return ('confirm', (), { 'orderID': self.pk })

	@models.permalink
	def getCancelURL(self):
		return ('cancel', (), { 'orderID': self.pk })

