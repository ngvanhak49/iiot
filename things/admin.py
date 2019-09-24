from django.contrib import admin

from .models import Thing, ThingData
# Register your models here.

class ThingsAdmin(admin.ModelAdmin):
    list_display = ('things_alt', 'name', 'things_address', 'description')

class ThingsDataAdmin(admin.ModelAdmin):
    search_fields = ('name', 'value')
    list_filter = ('name', 'created_date')
    readonly_fields = ('created_date',)
    ordering = ('-created_date',)
    date_hierarchy = 'created_date'
    list_display = ('id', 'name', 'value', 'created_date')

admin.site.register(Thing, ThingsAdmin)
admin.site.register(ThingData, ThingsDataAdmin)
