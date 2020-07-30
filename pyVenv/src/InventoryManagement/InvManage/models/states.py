# This files stores the states of the filter states of the tables
from django.db import models

class FilterState(models.Model):
    name = models.CharField(max_length=30)
    

class FilterColumn(models.Model):
    name = models.CharField(max_length=50)
    label = models.CharField(max_length=50)
    visible = models.BooleanField(null=True,default=True)
    position = models.IntegerField()
    state = models.ForeignKey(FilterState,on_delete=models.CASCADE)


