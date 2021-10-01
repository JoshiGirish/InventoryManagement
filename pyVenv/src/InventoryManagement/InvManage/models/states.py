# This files stores the states of the filter states of the tables
from django.db import models

class FilterState(models.Model):
    """Model of the filter state.

    Attributes
    ----------
    name : str
        Name of the filter state.
    """
    name = models.CharField(max_length=30)
    

class FilterColumn(models.Model):
    """Model of the column state.

    Attributes
    ----------
    name : str
        Name of the column.
    label : str
        Label of the column.
    visible : bool
        Visibility flag.
    position : int
        Index of the column.
    state : FilterState
        Primary key of the ``FilterState`` instance being referenced by the column instance.
    """
    name = models.CharField(max_length=50)
    label = models.CharField(max_length=50)
    visible = models.BooleanField(null=True,default=True)
    position = models.IntegerField()
    state = models.ForeignKey(FilterState,on_delete=models.CASCADE)


