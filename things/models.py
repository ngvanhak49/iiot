from django.db import models

# Create your models here.
from device.models import Device
# Create your models here.

THING_TYPE_CHOICES = (
    (1, 'Bit'),
    (2, 'Signed byte'),
    (3, 'Unsigned byte'),
    (4, 'Signed short'),
    (5, 'Unsigned short'),
    (6, 'Signed int32'),
    (7, 'Unsigned int32'),
    (8, 'Float'),
    (9, 'Signed int64'),
    (10, 'Unsigned int64'),
    (11, 'Double'),
)

THING_MASK_CHOICES = (
    (1, '1'),
    (2, 'F'),
)

THING_FCODE_CHOICES = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
    (6, '6'),
    (15, '15'),
    (16, '16'),
)

class Thing(models.Model):
    name = models.CharField(max_length=50)
    things_address = models.SmallIntegerField()
    things_type = models.SmallIntegerField(choices=THING_TYPE_CHOICES, default=5)
    things_fcode = models.SmallIntegerField(choices=THING_FCODE_CHOICES, default=4)
    things_mask = models.CharField(max_length=20, blank=True, default='FFFF')
    things_gain = models.FloatField(default=1)
    things_offset = models.FloatField(default=1)
    things_poll = models.SmallIntegerField(default=1000)
    description = models.TextField(blank=True)
    device_id = models.ForeignKey(Device, on_delete=models.CASCADE)
    things_alt = models.CharField(max_length=50, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Thing"

class ThingData(models.Model):
    things = models.ForeignKey(Thing, on_delete=models.CASCADE)
    value = models.CharField(max_length=20, blank=True)
    raw_value = models.CharField(max_length=20, blank=True)
    conv_value = models.CharField(max_length=20, blank=True) 
    created_date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50, blank=True, default=things.name)

    def __str__(self):
        return self.things.name

    class Meta:
        verbose_name = "Thing Data"