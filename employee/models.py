from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

class Employee(models.Model):
	username = models.CharField(max_length=255)
	allergies = models.CharField(blank=True, max_length=255, help_text='List any allergies you may have')
	diet = models.TextField(blank=True, help_text='List your dietary restrictions (vegetarion, vegan, kosher, halal)')

	def __unicode__(self):
		return self.user.username

class Order(models.Model):
    pass

def newUser(sender, instance, **kwargs):
	if kwargs['created']:
		new_employee = Employee()
		new_employee.save()

models.signals.post_save.connect(newUser, sender=User, dispatch_uid='employee.models')
