from django.db import models
from django.core.validators import *
import uuid


def randomGen():
    return int(str(uuid.uuid4().int)[:10])


class Charity(models.Model):
    username = models.CharField(primary_key=True,max_length=20)
    name = models.CharField(unique=True, max_length=100)
    address = models.CharField(max_length=300)
    description = models.CharField(max_length=500)


class Person(models.Model):
    charity = models.ForeignKey(Charity)
    tc_no = models.IntegerField(primary_key=True, unique=True, validators=[RegexValidator(r'\d{11,11}','Number must be 11 digits', 'Invalid number')])
    name = models.CharField(max_length=100)
    need = models.TextField(max_length=100)
    priority = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    description = models.TextField()
    
'''
class Category(models.Model):
    Person = models.ForeignKey(Person)
    mid = models.IntegerField(primary_key=True, default=randomGen())
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
'''