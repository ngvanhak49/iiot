from django.contrib import admin
from .models import RuleEngine

# Register your models here.
class RuleEngineAdmin(admin.ModelAdmin):
    list_display = ('id', 'thing', 'name', 'rule_type', 'rule_value', 'created_date')

admin.site.register(RuleEngine, RuleEngineAdmin)