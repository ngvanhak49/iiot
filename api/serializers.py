from rest_framework import serializers

from entry.models import Entry

class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = ['id', 'name', 'things', 'created_date', 'description']

from things.models import Thing

class ThingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thing
        fields = ['id', 'name', 'things_address', 'device_id', 'things_alt', 'created_date']