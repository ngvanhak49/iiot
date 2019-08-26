from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

from .serializers import (
    EntrySerializer, 
    ThingSerializer
)

from entry.models import Entry
class EntryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Entry.objects.all().order_by('-created_date')
    serializer_class = EntrySerializer

from things.models import Thing
class ThingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Thing.objects.all().order_by('-created_date')
    serializer_class = ThingSerializer
