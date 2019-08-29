from django.contrib import admin
from rulereport.models import RuleEngineReport

# Register your models here.
class RuleEngineReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'thing', 'name', 'ruleengine', 'value', 'created_date')

admin.site.register(RuleEngineReport, RuleEngineReportAdmin)