from rest_framework import serializers

from entry.models import Entry
from things.models import Thing, ThingData
from company.models import Company, Department
from ruleengine.models import RuleEngine
from rulereport.models import RuleEngineReport

class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = ['id', 'name', 'things', 'created_date', 'description']



class ThingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thing
        fields = '__all__'

class ThingDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThingData
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class RuleEngineSerializer(serializers.ModelSerializer):
    class Meta:
        model = RuleEngine
        fields = '__all__'

class RuleReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = RuleEngineReport
        fields = '__all__'