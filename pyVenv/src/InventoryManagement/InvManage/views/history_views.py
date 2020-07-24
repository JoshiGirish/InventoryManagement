from django.shortcuts import render
from django.shortcuts import redirect
from InvManage.models import EventCard
from InvManage.filters import EventCardFilter

def display_history_view(request):
    """   
    This function generates the history view.    
    """
    if request.method == 'GET':
        # Create a dictionary of all events
        events = EventCard.objects.all().order_by('-date')
        myFilter = EventCardFilter(request.GET, queryset=events)
        queryset = myFilter.qs
        dictionaries = []
        for event in queryset: 
            dictionaries.append(event.__dict__)   
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