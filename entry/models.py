from django.db import models

from things.models import Thing
from ruleengine.models import RuleEngine
from organization.models import Organization
# Create your models here.
class Entry(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(Organization, on_delete=models.CASCADE,  blank=True, null=True)
    things = models.ManyToManyField(Thing)
    attribute = models.CharField(max_length=50, blank=True) # Đặc tính của entry: (máy CNC, máy ép nhựa)
    #rules = models.ManyToManyField(RuleEngine)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Entry"