from django.db import models

from gateway.models import Gateway
# Create your models here.
class Device(models.Model):
    name = models.CharField(max_length=50, unique=True)
    dev_address = models.SmallIntegerField()
    description = models.TextField(blank=True)
    gateway_id = models.ForeignKey(Gateway, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'dev_address', 'description')
        verbose_name = "Device"