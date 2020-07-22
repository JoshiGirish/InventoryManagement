from InvManage.models import Object, EventCard
import datetime

def create_event(obj,event):
    modName = type(obj).__name__
    if modName == 'PurchaseOrder': # not all models have "name" field
        objName = '# '+ str(obj.po)
    elif modName == 'SalesOrder':
        objName = '# '+ str(obj.so)
    else:
        objName = obj.name
    # Create object associated with the event card
    newObj = Object.objects.create(identifier=obj.id, 
                                    name=objName, 
                                    model=type(obj).__name__)
    # Create event card
    newCard = EventCard.objects.create(obj=newObj, 
                                        objname=objName, 
                                        objmodel=type(obj).__name__, 
                                        date=datetime.datetime.now().strftime("%d/%m, %H:%M:%S"), 
                                        operation=event)
    