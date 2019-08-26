from django.db import models

# Create your models here.
class Gateway(models.Model):
    name = models.CharField(max_length=50)
    ip_address = models.CharField(max_length=20, blank=True)
    ip_mac = models.CharField(max_length=20, blank=True)
    ip_default = models.CharField(max_length=20, blank=True)
    ip_subnet = models.CharField(max_length=20, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Gateway"