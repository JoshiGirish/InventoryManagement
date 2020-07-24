from django.db import models
from django.utils import timezone


class Object(models.Model):
    identifier = models.CharField(null=True,max_length=100)
    name = models.CharField(null=True,max_length=100)
    model = models.CharField(null=True,max_length=100)


class EventCard(models.Model):
    obj = models.OneToOneField(Object,on_delete=models.SET_NULL,null=True)
    objId = models.CharField(null=True,max_length=100)
    objname = models.CharField(null=True,max_length=100)
    objmodel = models.CharField(null=True,max_length=100)
    date = models.TextField(null=True, blank=True)
    operation = models.CharField(null=True, blank=True,max_length=100)

