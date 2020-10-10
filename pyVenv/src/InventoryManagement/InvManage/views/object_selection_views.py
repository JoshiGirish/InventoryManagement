from django.shortcuts import render
from django.shortcuts import redirect
from InvManage.forms import *
from InvManage.models import *
from InvManage.filters import PurchaseOrderFilter
from django.http import JsonResponse
from InvManage.serializers import ProductSerializer, PPEntrySerializer, PurchaseInvoiceSerializer
from InvManage.scripts.filters import *
from InvManage.scripts.helpers import create_event

def get_purchase_orders_view(request):
    if request.method == 'GET':
        pos = PurchaseOrder.objects.all()
        state = FilterState.objects.get(name='POs_basic')
        column_list = change_column_position(request, state)
        myFilter = PurchaseOrderFilter(request.GET, queryset=pos)
        queryset = myFilter.qs
        number_of_objects = len(queryset)
        page_number = request.GET.get('page')
        page_obj, dictionaries = paginate(queryset, myFilter, page_number)
        # dictionary contains only vendor id and not vendor name. So add it.
        for dict in dictionaries:
            vend_id = dict['vendor_id']
            vendor = Vendor.objects.get(id=vend_id)
            dict['vendor'] = vendor.name
        return render(request, 'purchase_order/purchase_order_contents.html', {'page_obj': page_obj,
                                                                               'myFilter': myFilter,
                                                                               'n_prod': number_of_objects,
                                                                               'columns': column_list,
                                                                               'dicts': dictionaries,
                                                                               'url': request.build_absolute_uri('/purchase_orders/')})
