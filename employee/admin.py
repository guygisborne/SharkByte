from django.contrib import admin

from models import *

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'username', 'allergies', 'diet', 'card_number']

admin.site.register(Employee, EmployeeAdmin)
