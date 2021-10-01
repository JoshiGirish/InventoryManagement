from InvManage.models import Object, EventCard, ObjectModel, EventType
import datetime

def create_event(obj,event):
    """Creates an event card for each event.

    Parameters
    ----------
    obj : Model
        Model of the object instance being created, updated, or deleted.
    event : EventType
        Type of operation being performed on the object.
    """
    modName = type(obj).__name__
    if modName == 'PurchaseOrder': # not all models have "name" field
        objName = '# '+ str(obj.po)
    elif modName == 'GoodsReceiptNote':
        objName = '# '+ str(obj.identifier)
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

def get_parameter_list_from_request(req,parameter):
    """Extracts a parameter from the request.

    Parameters
    ----------
    req : HttpRequest
        The HTTP request.
    parameter : str
        The parameter being extracted.

    Returns
    -------
    List
        List of comma separated parameters. 
    """
    try:
        id_string= req.GET.get(parameter)
        param_list = list(map(int, id_string.split(',')))
    except (AttributeError, ValueError) as e:
        param_list = []
    return param_list

def generate_form_parameter_string(reqData):
    """Generates a paragraph element with the form data.

    Parameters
    ----------
    reqData : Dict
        Form data.

    Returns
    -------
    str
        HTML string rendered as form.
    """
    print(reqData.dict())
    d = reqData.dict()
    formString = ""
    # for form, data in enumerate(reqData):
    for key, value in d.items():
        formString += f"<p>:form {key}: ``{value}``\n</p>"
    return formString