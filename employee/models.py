from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

class Employee(models.Model):
	username = models.CharField(max_length=255, editable=False)
	display_name = models.CharField(blank=True, max_length=255, help_text='Name you\'re order will be under and called by')
	allergies = models.CharField(blank=True, max_length=255, help_text='List any allergies you may have')
	diet = models.TextField(blank=True, help_text='Describe your dietary restrictions (vegetarion, vegan, kosher, halal)')
	card_number = models.CharField(blank=True, max_length=255)
	pub_date = models.DateTimeField(auto_now_add=True, editable=False)

	def __unicode__(self):
		return (self.display_name if self.display_name else self.username)


