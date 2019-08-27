from django.contrib import admin

# Register your models here.
from .models import Customer, Contactor
# Register your models here.
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

class ContactorAdmin(admin.ModelAdmin):
    list_display = ('name', 'customer')

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Contactor, ContactorAdmin)