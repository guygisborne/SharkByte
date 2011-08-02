from django.contrib import admin

from models import *

class MealAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']


class TimeslotAdmin(admin.ModelAdmin):
    list_display = ['time', 'capacity']


class MenuAdmin(admin.ModelAdmin):
	list_display = ['type', 'description']
	filter_horizontal = ['meals', 'timeslots']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['employee', 'meal', 'instructions', 'isConfirmed']


admin.site.register(Timeslot, TimeslotAdmin)
admin.site.register(Meal, MealAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(Order, OrderAdmin)
