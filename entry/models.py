from django.db import models

from things.models import Thing
# Create your models here.
class Entry(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    things = models.ManyToManyField(Thing)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Entry"