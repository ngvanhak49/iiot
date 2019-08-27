from django.contrib import admin

# Register your models here.
from .models import Company, Department
# Register your models here.
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')

admin.site.register(Company, CompanyAdmin)
admin.site.register(Department, DepartmentAdmin)
