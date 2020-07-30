from django.shortcuts import render
from django.shortcuts import redirect
from InvManage.models import EventCard, HistoryFilterState
from InvManage.filters import EventCardFilter
from django.http import JsonResponse, HttpResponse
from django.template.response import TemplateResponse
from InvManage.serializers import HistoryFilterStateSerializer
from rest_framework.renderers import JSONRenderer
from InvManage.scripts.helpers import logger

def display_history_view(request):
    """   
    This function generates the history view.    
    """
    if request.method == 'GET':
        # Create a dictionary of all events
        events = EventCard.objects.all().order_by('-date') # Fetches event cards ordering them with recent events first
        logger(request.GET)
        # Get filter parameters
        myFilter = EventCardFilter(request.GET, queryset=events)
        queryset = myFilter.qs
        logger(queryset)
        dictionaries = []
        for event in queryset: 
            dictionaries.append(event.__dict__) 
            # logger(event.__dict__)  
        # Create a lookup dictionary for urls to be embedded in the event cards
        lookup = {'Company':'/company/update',
                  'Vendor': '/vendor/update',
                  'Consumer': '/consumer/update',
                  'Product': '/product/update',
                  'PurchaseOrder': '/purchase_order/update',
                  'SalesOrder': '/sales_order/update'}
        return render(request, 'history/history.html',{'dicts': dictionaries,
                                                       'lookupRoute':lookup,
                                                       'myFilter':myFilter})
        
    if request.method == 'POST':
        print(request.POST)
        # Get the state that needs to be updated
        state = HistoryFilterState.objects.all().first()
        # Update the state eventtypes
        eventlist = request.POST.getlist('operation')
        eventtype = state.eventtype_set.all().first()
        eventtype.created = True if ('create' in eventlist) else False
        eventtype.updated = True if ('update' in eventlist) else False
        eventtype.deleted = True if ('delete' in eventlist) else False
        eventtype.save()
        # Update the state objmodels
        objlist = request.POST.getlist('objmodel')
        models = state.objectmodel_set.all().first()
        models.company = True if ('Company' in objlist) else False
        models.vendor = True if ('Vendor' in objlist) else False
        models.po = True if ('PurchaseOrder' in objlist) else False
        models.product = True if ('Product' in objlist) else False
        models.consumer = True if ('Consumer' in objlist) else False
        models.so = True if ('SalesOrder' in objlist) else False
        models.save()
        return HttpResponse(status=204) 