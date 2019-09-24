from django.db import models
from customer.models import Customer

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=125,unique=True, verbose_name="name")
    #parent_company = models.ForeignKey('self', blank=True, null=True, related_name="children")
    owner = models.ForeignKey(Customer, on_delete=models.CASCADE,  blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name="children", verbose_name="parent company")
    description = models.CharField(max_length=250, blank=True, verbose_name=("description"))
    address = models.CharField(max_length=125, blank=True, null=True, verbose_name=("address"))
    city = models.CharField(max_length=50, blank=True, null=True, verbose_name=("city"))
    state = models.CharField(max_length=10,blank=True, null=True, verbose_name=("state"))
    zip_code = models.CharField(max_length=7, blank=True, null=True, verbose_name=("zip code"))
    importance = models.PositiveSmallIntegerField(default=99, verbose_name=("importance"))
    latitude = models.FloatField(blank=True, null=True, verbose_name=("latitude"))
    longitude = models.FloatField(blank=True, null=True,verbose_name=("longitude"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name=("created date"))
    date_modified = models.DateTimeField(auto_now=True, verbose_name=("date modified"))

    class Meta:
        verbose_name = 'company'
        verbose_name_plural = 'companies'
        ordering = ('-name',)

    def __unicode__(self):
        return "%s" %(self.name)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=125,verbose_name=("name"))
    #director = models.ForeignKey(Account, verbose_name=_("director"))
    belong_to = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="Company", verbose_name=("company belongs to"))
    #parent_department = models.ForeignKey('self', blank=True, null=True, related_name="children")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name="children", verbose_name=("parent department"))
    description = models.CharField(max_length=250, blank=True, verbose_name=("description"))
    telephone = models.CharField(max_length=20, blank=True, null=True, verbose_name=("telephone"))
    address = models.CharField(max_length=125, blank=True, null=True, verbose_name=("address"))
    city = models.CharField(max_length=50, blank=True, null=True, verbose_name=("city"))
    state = models.CharField(max_length=10,blank=True, null=True, verbose_name=("state"))
    zip_code = models.CharField(max_length=7, blank=True, null=True, verbose_name=("zip code"))
    importance = models.PositiveSmallIntegerField(default=99, verbose_name=("importance"))
    latitude = models.FloatField(blank=True, null=True, verbose_name=("latitude"))
    longitude = models.FloatField(blank=True, null=True,verbose_name=("longitude"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name=("created date"))
    date_modified = models.DateTimeField(auto_now=True, verbose_name=("date modified"))

    class Meta:
        verbose_name = 'department'
        verbose_name_plural = 'departments'
        ordering = ('name', 'importance')

    def __unicode__(self):
        return "%s(%d)" %(self.name, self.importance)
    
    def __str__(self):
        return self.name

    @property
    def employees_count(self):
        #return hr.models.Person.objects.filter(status__lte=10, job__department=self).count()
        pass