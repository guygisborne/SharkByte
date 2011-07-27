from django.contrib import admin

from models import *

class MenuAdmin(admin.ModelAdmin):
    list_display = ['description', 'expiration']

class MealToMenuAdmin(admin.ModelAdmin):
    list_display = ['meal', 'menu']

class MealAdmin(admin.ModelAdmin):
    list_display = ['name','description', 'meal_type']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['employee','meal','instructions','state']

class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ['time', 'capacity']

admin.site.register(Menu, MenuAdmin)
admin.site.register(MealToMenu, MealToMenuAdmin)
admin.site.register(Meal, MealAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(TimeSlot,TimeSlotAdmin)
