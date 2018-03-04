# -*- coding: utf-8 -*-
from API.models import Person, Charity
import re

class JSONPayload:
    def __init__(self, j):
        self.__dict__ = j

    def __getitem__(self, item):
        return self.__dict__[item]


class PersonSerializer:
    class Meta:
        model = Person
        fields = ('name', 'tc_no', 'need', 'description', 'priority')

    @staticmethod
    def check(data):
        response = {"availability": True, "errors": []}
        try:
            if not (1 <= int(data["priority"]) <=5):
                response["availability"] = False
                response["errors"].append("Öncelik 1 ile 5 arasinda bir değer olmalıdır.")
        except:
            response["availability"] = False
            response["errors"].append("Öncelik 1 ile 5 arasinda bir değer olmalıdır.")

        if len(re.findall(r"\d{11}",str(data["tc_no"]))) != 1:
            response["availability"] = False
            response["errors"].append("TC Kimlik No 11 haneli bir sayı olmalıdır.")

        if len(re.findall(r"\D",str(data["tc_no"]))) != 0:
            response["availability"] = False
            response["errors"].append("TC Kimlik No sadece sayılardan oluşmalıdır.")
        return response

    @staticmethod
    def serialize(obj, typ='DICT'):
        try:
            if typ == 'DICT':
                return {'tc_no': obj.tc_no, 'name': obj.name, 'need': obj.need.split(','),
                        'description': obj.description, 'priority': obj.priority}
            elif typ == 'LIST':
                return [obj.tc_no, obj.name, obj.need, obj.description, obj.priority]
        except Exception as e:
            return "Exception occurred: " + str(e)

    @staticmethod
    def deserialize(data, charity_username=None):
        try:
            new_obj = JSONPayload(data)
            charity = Charity.objects.get(username=charity_username)
            availability = PersonSerializer.check(data)

            if not availability["errors"]:
                p = Person.objects.create(name=new_obj['name'], tc_no=new_obj['tc_no'],
                                          need=new_obj['need'], description=new_obj['description'],
                                          priority=new_obj['priority'], charity=charity)
                p.save()
            return availability
        except Exception as e:
            print e
            return {"availability": False, "errors": ["Bu TC Kimlik No sistemde kayıtlı."]}

    @staticmethod
    def get_all(charity=None):
        items = Person.objects.filter(charity=Charity.objects.filter(name=charity['name']))
        serialized = {'data': [PersonSerializer.serialize(i, 'LIST') for i in items]}
        return serialized


class CharitySerializer:
    class Meta:
        model = Charity
        fields = ('username', 'name', 'address', 'description')

    @staticmethod
    def check(data):
        response = {"availability": True, "errors": []}
        return response

    @staticmethod
    def serialize(obj, typ='DICT'):
        try:
            if typ == 'DICT':
                return {'username': obj.username, 'name': obj.name,
                        'address': obj.address, 'description': obj.description}
            elif typ == 'LIST':
                return [obj.name, obj.address, obj.description]
        except Exception as e:
            return "Exception occurred: " + str(e)

    @staticmethod
    def deserialize(data, charity_username=None):
        try:
            new_obj = JSONPayload(data)
            p = Person.objects.create(username=new_obj['username'], name=new_obj['name'],
                                      address=new_obj['address'], description=new_obj['description'])
            p.save()
        except:
            return {"availability": True,"errors": []}


class Serializer:
    serializers = {'Person': PersonSerializer, 'Charity': CharitySerializer}

    def __init__(self, typ=None):
        self.serializer = self.serializers[typ]


