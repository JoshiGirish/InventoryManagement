from django.shortcuts import render
from django.shortcuts import redirect
from InvManage.models import EventCard, HistoryFilterState
from InvManage.filters import EventCardFilter
from django.http import JsonResponse, HttpResponse
from django.template.response import TemplateResponse
from InvManage.serializers import HistoryFilterStateSerializer
from rest_framework.renderers import JSONRenderer
from InvManage.forms import HistoryForm
import json

def display_history_view(request):
    """ 
        Retrieves the list of events on ``GET`` request. The ``create``, ``update``, and ``delete`` events are registered for each model.

        .. http:get:: /history/

            Gets the list of all history items.

            **Example request**:

            .. sourcecode:: http

                GET /history/ HTTP/1.1
                Host: localhost:8000
                Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
                
                [
                    {
                        "objname": {
                            ""
                        },
                        "operation": {
                            "Created",
                            "Updated",
                            "Deleted"
                        },
                        "objmodel": {
                            "Company",
                            "Vendor",
                            "PurchaseOrder",
                            "Product",
                            "Consumer",
                            "SalesOrder",
                            "GoodsReceiptNote"
                        },
                        "history-qlen": {
                            "10"
                        },
                        "date__gt": {
                            "11/01/2020"
                        },
                        "date__lt": {
                            "09/26/2021"
                        }
                    }
                ]

    
            **Example response**:

            .. sourcecode:: http

                HTTP/1.1 200 OK
                Vary: Accept
                Content-Type: text/html; charset=utf-8

            :reqheader Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
            :statuscode 200: List of filtered history events received successfully.
    """
    if request.method == 'GET':
        # Create a dictionary of all events
        events = EventCard.objects.all().order_by('-date') # Fetches event cards ordering them with recent events first
        qlenForm = HistoryForm(request.GET, prefix='history')
        # Get filter parameters
        state = HistoryFilterState.objects.all().first() # Get saved filter state
        if len(request.GET) == 0: # on page reload their are no parameters in the request
            jsonDec = json.decoder.JSONDecoder() # Instantiate decoder
            filterParams = jsonDec.decode(state.params) # Decode JSON string to python dictionary
            myFilter = EventCardFilter(filterParams, queryset=events)
            queryset = myFilter.qs[:int(filterParams['history-qlen'])]
            qlenForm = HistoryForm({'history-qlen':int(filterParams['history-qlen'])})
        else:
            if qlenForm.is_valid():
                qlen = qlenForm.cleaned_data['qlen']
            params = {
                'operation' : request.GET.getlist('operation'),
                'objmodel' : request.GET.getlist('objmodel'),
                'date__gt' : request.GET.get('date__gt'),
                'date__lt' : request.GET.get('date__lt'),
                'history-qlen' : qlen
            }
            state.params = json.dumps(params)
            state.save()        
            myFilter = EventCardFilter(request.GET, queryset=events)
            queryset = myFilter.qs[:int(request.GET['history-qlen'])]
        dictionaries = []
        for event in queryset: 
            dictionaries.append(event.__dict__) 
        # Create a lookup dictionary for urls to be embedded in the event cards
        lookup = {'Company':'/company/update',
                  'Vendor': '/vendor/update',
                  'Consumer': '/consumer/update',
                  'Product': '/product/update',
                  'PurchaseOrder': '/purchase_order/update',
                  'SalesOrder': '/sales_order/update',
                  'GoodsReceiptNote':'/grn/update'}
        return render(request, 'history/history.html',{'dicts': dictionaries,
                                                       'lookupRoute':lookup,
                                                       'myFilter':myFilter,
                                                       'qlenForm': qlenForm})
