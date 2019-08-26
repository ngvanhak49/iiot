from django.contrib import admin

from .models import Thing, Data
# Register your models here.

class ThingsAdmin(admin.ModelAdmin):
    list_display = ('things_alt', 'name', 'things_address', 'description')

class ThingsDataAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'created_date')

admin.site.register(Thing, ThingsAdmin)
admin.site.register(Data, ThingsDataAdmin)
