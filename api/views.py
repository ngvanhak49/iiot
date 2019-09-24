from django.shortcuts import render
from django.core import serializers

# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import generics
from django.forms.models import model_to_dict

import datetime
import json

from .serializers import (
    EntrySerializer, 
    ThingSerializer,
    ThingDataSerializer,
    CompanySerializer,
    DepartmentSerializer,
    RuleEngineSerializer,
    RuleReportSerializer,
    CustomerSerializer,
    OrganizationSerializer,
)

from company.models import Company, Department
from things.models import Thing, ThingData
from entry.models import Entry
from rulereport.models import RuleEngineReport
from ruleengine.models import RuleEngine
from customer.models import Customer
from organization.models import Organization

from .utils import (
    util_debugger,
    get_entrydata,
    get_entrydata_all,
    get_thingdata_bytime,
    get_thingdata_last,
)


class EntryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Entry.objects.all().order_by('-created_date')
    serializer_class = EntrySerializer

    @action(detail=False)
    def data(self, request):
        name = request.query_params.get('id', None)
        start = request.query_params.get('start', None)
        end = request.query_params.get('end', None)
        
        schedule = Entry.objects.get(pk=name)

        dic = get_entrydata(schedule, start, end)
 
        return Response(dic)

    @action(detail=False)
    def ownerdata(self, request):
        OrganizationID = self.request.query_params.get('id', None)
        member = Organization.objects.get(pk=OrganizationID)
        #childrens = Organization.objects.get(pk=1).children.all()

        members = [member]
        members = member.get_all_children(members)
        entries = []
        for member in members:
            eo = Entry.objects.all()
            et = eo.filter(owner=member.id)
            if et.exists(): 
                for item in et:
                    dic = get_entrydata(item, None, None)
                    entries.append(dic)
        util_debugger(entries)
        #rets = EntrySerializer(entries, many=True)
        #rets = serializers.serialize('json', entries)
        # rets = EntrySerializer(entries, many=True).data
        # rets['things'] = things_data
        # util_debugger(rets)
        return Response(entries)

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

    #   api/ThingDataViewSet?thing=name&start=yyyy-mm-ddTHH:MM:SS?end=...
    @action(detail=True)
    def thing(self, request):
        name = request.query_params.get('name', None)
        start = request.query_params.get('start', None)
        end = request.query_params.get('end', None)
        schedule = self.queryset.filter(name=name)
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

class CustomerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Customer.objects.all().order_by('-created_date')
    serializer_class =    CustomerSerializer

class OrganizationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Organization.objects.all().order_by('-created_date')
    serializer_class =    OrganizationSerializer
    #   api/organization/tree?id=name
    @action(detail=False)
    def tree(self, request):

        OrganizationID = request.query_params.get('id', None)
        member = Organization.objects.get(pk=OrganizationID)
        # childrens = Organization.objects.get(pk=OrganizationID).children.all()
        util_debugger(member)
        # print(childrens)
        # ser_member = serializers.serialize('json', {member })
        # print(ser_member)
        # print("*************************")
        # ser_childrens = serializers.serialize('json', {childrens[0], childrens[1]})
        # print(ser_childrens)

        # print("==========================")
        # serialized_data = serializers.serialize('json', [member], use_natural_foreign_keys=True, fields=['parent'])
        # print(serialized_data)
        #olist = [member]
        #organizate = self.get_all_children()
        members = {member}
        #members = member.get_all_children(members)
        #members = member.get_all_children_json(members)

        members = member.get_family_tree(member) # return list dict member owned by organization id.
        util_debugger(members)
        #print("______________________________")
        #members = json.dumps(members)
        #print(members)
        #abc = OrganizationSerializer(abc, many=False)

        if OrganizationID is None:
            return []
        else:
            return Response(members)    # auto convert json format.

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
    #   api/thingrulereport?thing=name&start=yyyy-mm-ddTHH:MM:SS?end=...
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
                
class v1_CustomerViewSet(generics.ListAPIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = CustomerSerializer

    #permission_classes = [IsOwner]

    def get_queryset(self):
        customer_id = self.request.query_params.get('customer', None)
        customer = Customer.objects.get(customer_id)
        companies = Company.objects.all().order_by('-created_date').filter(owner=customer_id)

        if customer is None:
            return queryset
        else:
            return queryset.filter(id=customer_id)

class v1_CompanyViewSet(generics.ListAPIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = CompanySerializer

    #permission_classes = [IsOwner]

    def get_queryset(self):
        queryset = Company.objects.all().order_by('-created_date')
        customer = self.request.query_params.get('customer', None)

        if customer is None:
            return []
        else:
            return queryset.filter(owner=customer)

############# business api #####################################

class v1_OrganizationByIDViewSet(generics.ListAPIView):
    serializer_class = OrganizationSerializer

    #permission_classes = [IsOwner]

    def get_queryset(self):
        OrganizationID = self.request.query_params.get('id', None)
        member = Organization.objects.get(pk=OrganizationID)
        #childrens = Organization.objects.get(pk=1).children.all()

        members = [member]
        members = member.get_all_children(members)
        print(members)
        return members

'''
v1_EntryByOwnerViewSet:
    return list entries in owner and children of owner.
'''
class v1_EntryByOwnerViewSet(generics.ListAPIView):
    serializer_class = EntrySerializer

    #permission_classes = [IsOwner]

    def get_queryset(self):
        OrganizationID = self.request.query_params.get('id', None)
        member = Organization.objects.get(pk=OrganizationID)
        #childrens = Organization.objects.get(pk=1).children.all()

        members = [member]
        members = member.get_all_children(members)
        entries = []
        for member in members:
            eo = Entry.objects.all()
            et = eo.filter(owner=member.id)
            if et.exists(): 
                for item in et:
                    entries.append(item)
        util_debugger(entries)
        #rets = EntrySerializer(entries, many=True)
        #rets = serializers.serialize('json', entries)
        rets = EntrySerializer(entries, many=True)
        util_debugger(rets)
        return entries


#--------------------------------------------------------------------#
# class OrganizationByIDViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = Organization.objects.all().order_by('-created_date')
#     serializer_class = OrganizationSerializer

#     #   api/ThingDataViewSet?thing=name&start=yyyy-mm-ddTHH:MM:SS?end=...
#     @action(detail=False)
#     def all(self, request):
#         #return Response([])
#         OrganizationID = request.query_params.get('id', None)
#         member = Organization.objects.get(pk=OrganizationID)
#         childrens = Organization.objects.get(pk=1).children.all()
#         print(member)
#         print(childrens)
#         ser_member = serializers.serialize('json', {member })
#         print(ser_member)
#         print("*************************")
#         ser_childrens = serializers.serialize('json', {childrens[0], childrens[1]})
#         print(ser_childrens)

#         print("==========================")
#         serialized_data = serializers.serialize('json', [member], use_natural_foreign_keys=True, fields=['parent'])
#         print(serialized_data)
#         #olist = [member]
#         #organizate = self.get_all_children()
#         members = {member}
#         #members = member.get_all_children(members)
#         #members = member.get_all_children_json(members)

#         members = member.get_family_tree(member)
#         print(members)
#         #print("______________________________")
#         #members = json.dumps(members)
#         #print(members)
#         #abc = OrganizationSerializer(abc, many=False)

#         if OrganizationID is None:
#             return []
#         else:
#             return Response(members)

   

# class v1_OrganizationViewSet(generics.ListAPIView):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     serializer_class = OrganizationSerializer
#     queryset = {}
#     #permission_classes = [IsOwner]

#     def get_queryset(self):
#     #@action(detail=True)
#     #def item(self, request):
#         OrganizationID = self.request.query_params.get('id', None)
#         member = Organization.objects.get(pk=OrganizationID)
#         childrens = Organization.objects.get(pk=1).children.all()
#         print(member)
#         print(childrens)
#         ser_member = serializers.serialize('json', {member })
#         print(ser_member)
#         print("*************************")
#         ser_childrens = serializers.serialize('json', {childrens[0], childrens[1]})
#         print(ser_childrens)

#         print("==========================")
#         serialized_data = serializers.serialize('json', [member], use_natural_foreign_keys=True, fields=['parent'])
#         print(serialized_data)
#         #olist = [member]
#         #organizate = self.get_all_children()
#         members = {member}
#         #members = member.get_all_children(members)
#         #members = member.get_all_children_json(members)

#         members = member.get_family_tree(member)
#         print(members)
#         print("______________________________")
#         abc = json.dumps(members)
#         print(members)
#         abc = OrganizationSerializer(abc, many=False)

#         if OrganizationID is None:
#             return []
#         else:
#             return members
