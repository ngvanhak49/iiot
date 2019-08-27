from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from .serializers import (
    EntrySerializer, 
    ThingSerializer,
    ThingDataSerializer,
    CompanySerializer,
    DepartmentSerializer,
)

from company.models import Company, Department

from entry.models import Entry
class EntryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Entry.objects.all().order_by('-created_date')
    serializer_class = EntrySerializer

from things.models import Thing, ThingData
class ThingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Thing.objects.all().order_by('-created_date')
    serializer_class = ThingSerializer

class ThingDataViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = ThingData.objects.all().order_by('-created_date')
    serializer_class = ThingDataSerializer
    #permission_classes = [IsOwner]

    @action(detail=True)
    def data_list(self, request, pk=None):
        #data = self.get_object() # retrieve an object by pk provided
        schedule = ThingData.objects.filter(things_id=pk).distinct()[:1]
        schedule_json = ThingDataSerializer(schedule, many=True)
        return Response(schedule_json.data)

class CompanyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Company.objects.all().order_by('-created_date')
    serializer_class = CompanySerializer

class DeparmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Department.objects.all().order_by('-created_date')
    serializer_class = DepartmentSerializer