from django.core import serializers

# Create your views here.
from django.forms.models import model_to_dict
from django.db.models import Q

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

def util_debugger(*values: object):
    print(values)

def get_thing_ruleengine(thing):
    rules = RuleEngine.objects.all().filter(thing=thing)
    dic = RuleEngineSerializer(rules, many=True).data
    return dic

def get_thingdata_last(thing):
    dict_thing = ThingSerializer(thing).data# model_to_dict(thing)
    id = dict_thing.get('id')
    data = ThingData.objects.all().order_by('-created_date').filter(things_id=id).first()
    d = ThingDataSerializer(data).data #model_to_dict(data)
    util_debugger(d)
    dict_thing['value'] = d

    rules = get_thing_ruleengine(thing)
    dict_thing['rules'] = rules

    return dict_thing

def get_thingdata_bytime(thing, start, end):
    dict_thing = ThingSerializer(thing).data #model_to_dict(thing)
    id = dict_thing.get('id')
    data = ThingData.objects.all().order_by('-created_date').filter(things_id=id, created_date__range=(start,end))

    dict_thing['value'] = ThingDataSerializer(data, many=True).data #dc

    rules = get_thing_ruleengine(thing)
    dict_thing['rules'] = rules

    return dict_thing

def get_entrydata(entry, start, end):
    if entry is not None:
        dict_entry = model_to_dict(entry)
        util_debugger(dict_entry)

        things = dict_entry.get('things')
        things_data = []
        for thing in things:
            if start is not None:
                if end is None: end = datetime.datetime.now()
                da = get_thingdata_bytime(thing, start, end)
            else:
                da = get_thingdata_last(thing)
            things_data.append(da)

        dict_entry['things'] =  things_data
        util_debugger(dict_entry)

        return dict_entry
    return []

def get_entrydata_all(entry, start, end):
    if entry is not None:
        dict_entry = model_to_dict(entry)
        util_debugger(dict_entry)
        things = dict_entry.get('things')
        filter_stat = None
        things_dicts = []
        for thing in things:
            dict_thing = ThingSerializer(thing).data
            things_dicts.append(dict_thing)
            id = dict_thing.get('id')
            if filter_stat is None: filter_stat = Q(things_id=id)
            else: filter_stat |= Q(things_id=id)
        #util_debugger(filter_stat)

        query = ThingData.objects.all().order_by('-created_date').filter(filter_stat, created_date__range=(start,end))
        # data = ThingDataSerializer(query).data
        # print(data)
        dic_data = ThingDataSerializer(d, many=True).data
        # for d in query:
        #     #for ri in d:
        #     #    dd = ThingDataSerializer(ri).data
        #     #    r.append(dd)
        #     dd = ThingDataSerializer(d).data
        #     dic_data.append(dd)
        # #util_debugger(dic_data)
        
        return dic_data
    return []