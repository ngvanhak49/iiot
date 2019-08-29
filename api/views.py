from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import generics

import datetime

from .serializers import (
    EntrySerializer, 
    ThingSerializer,
    ThingDataSerializer,
    CompanySerializer,
    DepartmentSerializer,
    RuleEngineSerializer,
    RuleReportSerializer,
)

from company.models import Company, Department
from things.models import Thing, ThingData
from entry.models import Entry
from rulereport.models import RuleEngineReport
from ruleengine.models import RuleEngine

class EntryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Entry.objects.all().order_by('-created_date')
    serializer_class = EntrySerializer


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
    def last(self, request, pk=None):
        #data = self.get_object() # retrieve an object by pk provided
        schedule = self.queryset.filter(things_id=pk).distinct()[:1]
        schedule_json = ThingDataSerializer(schedule, many=True)
        return Response(schedule_json.data)

    @action(detail=True)
    def thing(self, request, pk=None):
        thing = pk
        start = request.query_params.get('start', None)
        end = request.query_params.get('end', None)
        schedule = self.queryset.filter(things_id=thing)
        if start is not None:
            if end is None: end = datetime.datetime.now()
            schedule = schedule.filter(created_date__range=(start,end))

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

class RuleEngineViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = RuleEngine.objects.all().order_by('-created_date')
    serializer_class = RuleEngineSerializer

class ThingRuleReportViewSet(generics.ListAPIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    #queryset = RuleEngineReport.objects.all().order_by('-created_date')
    serializer_class = RuleReportSerializer

    #permission_classes = [IsOwner]
    # def list(self, request):
    #     queryset = RuleEngineReport.objects.all().order_by('-created_date')
    #     serializer_class = RuleReportSerializer(queryset, many=True)
    #     return Response(serializer_class.data)
    def get_queryset(self):
        queryset = RuleEngineReport.objects.all().order_by('-created_date')
        thing = self.request.query_params.get('thing', None)
        start = self.request.query_params.get('start', None)
        end = self.request.query_params.get('end', None)

        if thing is None:
            return queryset
        else:
            if start is None:
                return queryset.filter(thing_id=thing)
            else:
                if end is None: end = datetime.datetime.now()
                return queryset.filter(thing_id=thing, created_date__range=(start, end))
                
