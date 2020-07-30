from InvManage.models import Object, EventCard, ObjectModel, EventType
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
                                    model=modName)
    # Create event card
    newCard = EventCard.objects.create(obj=newObj, 
                                        objId=obj.id,
                                        objname=objName, 
                                        objmodel=modName, 
                                        operation=event,
                                        date=datetime.datetime.now())
                                        # date=datetime.datetime.now().strftime("%d/%m, %H:%M:%S"))
    # print(modName)
    # objmod = ObjectModel.objects.get(modName=modName)
    # newCard.objmodel.add(objmod)
    # newCard.save()
    # evetyp = EventType.objects.get(label=event)
    # newCard.operation.add(evetyp)
    # newCard.save()

def logger(data):
    print('####################################')
    print('#')
    print('#')
    print('#')
    
    print(data)
    
    print('#')
    print('#')
    print('#')
    print('####################################')
    
            
