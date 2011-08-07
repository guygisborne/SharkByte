from datetime import datetime

from django.db import models

class Employee(models.Model):
	username = models.CharField(max_length=255, editable=False)
	full_name = models.CharField(max_length=255, help_text='Orders will be placed under this name')
	allergies = models.CharField(blank=True, max_length=255)
	diet = models.TextField(blank=True)
	card_number = models.CharField(blank=True, max_length=255)
	pub_date = models.DateTimeField(auto_now_add=True, editable=False)

	def __unicode__(self):
		return self.full_name
	
