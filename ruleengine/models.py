from django.db import models
from things.models import Thing

# Create your models here.

RULE_TYPE_CHOICES = (
    (1, 'equal'),
    (2, 'upper'),
    (3, 'lower'),
    (4, 'in range'),
    (5, 'out range'),
    (6, 'null'),
)

class RuleEngine(models.Model):
    thing = models.ForeignKey(Thing, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True, default=thing.name)
    rule_type = models.SmallIntegerField(choices=RULE_TYPE_CHOICES, default=1)
    rule_value = models.CharField(max_length=50, blank=True, default='')
    created_date = models.DateTimeField(auto_now_add=True)    

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Rule Engine"