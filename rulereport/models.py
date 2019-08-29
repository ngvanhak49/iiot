from django.db import models

from things.models import Thing
from ruleengine.models import RuleEngine
# Create your models here.

class RuleEngineReport(models.Model):
    thing = models.ForeignKey(Thing, on_delete=models.CASCADE)
    ruleengine = models.ForeignKey(RuleEngine, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True, default=thing.name)
    value = models.CharField(max_length=50, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)    

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Rule Engine Report"