from django.shortcuts import render
from django.shortcuts import redirect
from InvManage.models import EventCard

def display_history_view(request):
    """   
    This function generates the history view.    
    """
    if request.method == 'GET':
        # Create a dictionary of all events
        events = EventCard.objects.all().order_by('-date')
        dictionaries = []
        for event in events: 
            dictionaries.append(event.__dict__)   
        # Create a lookup dictionary for urls to be embedded in the event cards
        lookup = {'Company':'/company/update',
                  'Vendor': '/vendor/update',
                  'Consumer': '/consumer/update',
                  'Product': '/product/update',
                  'PurchaseOrder': '/purchase_order/update',
                  'SalesOrder': '/sales_order/update'}
        return render(request, 'history/history.html',{'dicts': dictionaries,'lookupRoute':lookup})