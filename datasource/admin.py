from django.contrib import admin

from .models import datasource

# Register your models here.
class DataSourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'host', 'port')

admin.site.register(datasource, DataSourceAdmin)