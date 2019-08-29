from django.db import models

# Create your models here.
TYPE_CHOICES = (
    (1, "SOCKET"),
    (2, "OPC"),
    (3, "MQTT"),
    (4, "Modbus"),
    (5, "Others")
)

class datasource(models.Model):
    version = models.SmallIntegerField(default=1)
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=128)
    type = models.SmallIntegerField(choices=TYPE_CHOICES, default=3)
    host = models.CharField(max_length=128)
    port = models.SmallIntegerField()
    user_name = models.CharField(max_length=64, blank=True)
    password = models.CharField(max_length=64, blank=True)
    end_path = models.CharField(max_length=128, blank=True)
    security = models.CharField(max_length=64, blank=True)
    mesg_mode = models.CharField(max_length=64, blank=True)
    keystore = models.CharField(max_length=128, blank=True)
    keystore_pass = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "DataSource"
