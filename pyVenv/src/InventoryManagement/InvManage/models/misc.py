from django.db import models
from django.utils import timezone


class Object(models.Model):
    identifier = models.CharField(null=True,max_length=100)
    name = models.CharField(null=True,max_length=100)
    model = models.CharField(null=True,max_length=100)


class EventType(models.Model):
    name = models.CharField(max_length=100)
    label = models.CharField(max_length=30)
    
    
    def __str__(self):
        return self.label


class ObjectModel(models.Model):
    name = models.CharField(max_length=100)
    label = models.CharField(max_length=30)
    modName = models.CharField(max_length=30)
    
    def __str__(self):
        return self.label
    

class EventCard(models.Model):
    obj = models.OneToOneField(Object,on_delete=models.SET_NULL,null=True)
    objId = models.CharField(null=True,max_length=100)
    objname = models.CharField(null=True,max_length=100)
    objmodel = models.CharField(null=True, max_length=100)
    date = models.DateTimeField(null=True, blank=True)
    operation = models.CharField(null=True, max_length=100)


class HistoryFilterState(models.Model):
    params = models.TextField(null=True) # Field to store serialized the state parameters
