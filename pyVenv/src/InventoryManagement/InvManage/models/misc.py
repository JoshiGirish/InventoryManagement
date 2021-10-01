from django.db import models
from django.utils import timezone


class Object(models.Model):
    """Model for a generic object.

    Attributes
    ----------
    identifier : str
        Unique identifier of the object.
    name : str
        Name of the object.
    model : str
        Model associated with the object.
    """
    identifier = models.CharField(null=True,max_length=100)
    name = models.CharField(null=True,max_length=100)
    model = models.CharField(null=True,max_length=100)


class EventType(models.Model):
    """Model for event type.

    Attributes
    ----------
    name : str
        Name of the event being triggered.
    label : str
        Label associated with the event.
    
    Returns
    -------
    Label
        Returns the string representation of the label when the event type is queried.
    """
    name = models.CharField(max_length=100)
    label = models.CharField(max_length=30)
    
    
    def __str__(self):
        return self.label


class ObjectModel(models.Model):
    """Model associated with an object.

    Attributes
    ----------
    name : str
        Name of the object.
    label : str
        Label string of the object.
    modName : str
        Name of the model associated with the object.

    Returns
    -------
    Label
        Returns string representation of the label when object model is queried.
    """
    name = models.CharField(max_length=100)
    label = models.CharField(max_length=30)
    modName = models.CharField(max_length=30)
    
    def __str__(self):
        return self.label
    

class EventCard(models.Model):
    """Model for event card to be displayed in the history view.

    Attributes
    ----------
    obj : OneToOneField
        Object associated with the event.
    objId : str
        Unique identifier of the object.
    objname : str
        Name of the object.
    objmodel : str
        Model of the object.
    date : DateField
        Timestamp of the event.
    operation : str
        Type of event.
    """
    obj = models.OneToOneField(Object,on_delete=models.SET_NULL,null=True)
    objId = models.CharField(null=True,max_length=100)
    objname = models.CharField(null=True,max_length=100)
    objmodel = models.CharField(null=True, max_length=100)
    date = models.DateTimeField(null=True, blank=True)
    operation = models.CharField(null=True, max_length=100)


class HistoryFilterState(models.Model):
    """Model of filter state of the history.

    Attributes
    ----------
    params : str
        Paramameters of the configured filters.
    """
    params = models.TextField(null=True) # Field to store serialized the state parameters
