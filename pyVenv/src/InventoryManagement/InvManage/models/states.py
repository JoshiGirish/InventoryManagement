# This files stores the states of the filter states of the tables
from django.db import models

class ProductFilterState(models.Model):
    name = models.CharField(max_length=30)

class ProductFilterColumn(models.Model):
    name = models.CharField(max_length=50)
    label = models.CharField(max_length=50)
    visible = models.BooleanField(default=True)
    position = models.IntegerField()
    state = models.ForeignKey(ProductFilterState,on_delete=models.CASCADE)