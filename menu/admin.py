from django.contrib import admin

from models import *

class TimeslotAdmin(admin.ModelAdmin):
    list_display = ['time', 'capacity']


class MealAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']


class MenuAdmin(admin.ModelAdmin):
	list_display = ['type', 'description', 'publish_date']
	filter_horizontal = ['meals', 'timeslots']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['employee', 'meal', 'instructions', 'state']


admin.site.register(Timeslot, TimeslotAdmin)
admin.site.register(Meal, MealAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(Order, OrderAdmin)
