from django.contrib import admin

from models import *

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['username', 'allergies', 'diet']

admin.site.register(Employee, EmployeeAdmin)
