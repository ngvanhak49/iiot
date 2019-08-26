from django.db import models

# Create your models here.
from device.models import Device
# Create your models here.
class Thing(models.Model):
    name = models.CharField(max_length=50)
    things_address = models.SmallIntegerField()
    things_type = models.CharField(max_length=50, blank=True, default='Unsinged short')
    things_fcode = models.SmallIntegerField(default=4)
    things_mask = models.CharField(max_length=20, blank=True, default='FFFF')
    things_gain = models.FloatField(default=1)
    things_offset = models.FloatField(default=1)
    things_poll = models.SmallIntegerField(default=1000)
    description = models.TextField(blank=True)
    device_id = models.ForeignKey(Device, on_delete=models.CASCADE)
    things_alt = models.CharField(max_length=50)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Thing"

class ThingData(models.Model):
    things = models.ForeignKey(Thing, on_delete=models.CASCADE)
    value = models.CharField(max_length=20, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50, blank=True, default=things.name)

    def __str__(self):
        return self.things.name

    class Meta:
        verbose_name = "Thing Data"