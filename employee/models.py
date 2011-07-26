from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

class Employee(models.Model):
	username = models.CharField(max_length=255)
	allergies = models.CharField(blank=True, max_length=255, help_text='List any allergies you may have.')
	diet = models.TextField(blank=True, help_text='List your dietary restrictions (vegetarion, vegan, kosher, halal).')
	pub_date = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.username


