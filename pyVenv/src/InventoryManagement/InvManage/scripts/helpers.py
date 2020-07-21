from InvManage.models import Object, EventCard
import datetime

def create_event(obj,event):
    # Create object associated with the event card
    new_obj = Object.objects.create(obj.pk, obj.name, type(obj), obj.description)
    # Create event card
    new_card = EventCard.objects.create(new_obj,datetime.datetime.now(),event)
    