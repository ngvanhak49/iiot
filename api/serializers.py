from rest_framework import serializers

from entry.models import Entry

class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = ['id', 'name', 'things', 'created_date', 'description']

from things.models import Thing, ThingData

class ThingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thing
        fields = ['id', 'name', 'things_address', 'device_id', 'things_alt', 'created_date']

class ThingDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThingData
        fields = '__all__'

from company.models import Company, Department
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'