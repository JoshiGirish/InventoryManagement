from django.shortcuts import render
from django.shortcuts import redirect
from InvManage.forms import *
from django.forms.formsets import formset_factory
from InvManage.models import *
from django.core.files.storage import FileSystemStorage
import io
import csv
from InvManage.filters import ProductFilter, VendorFilter, PurchaseOrderFilter, CompanyFilter
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.db import IntegrityError, transaction
from InvManage.serializers import VendorSerializer, PPEntrySerializer, PurchaseOrderSerializer, InvoiceSerializer, ProductSerializer
from InvManage.scripts.filters import *


def create_vendor_view(request):
    if request.method == 'GET':
        vendors = []
        for i, vend in enumerate(Vendor.objects.all()):
            vendors.append(
                {'id': vend.id, 'name': vend.name, 'code': vend.identifier})
        vendor_form = VendorForm()
        return render(request, 'vendor.html', {'vendor_form': vendor_form, 'vendors': vendors, 'requested_view_type': 'create'})
    if request.method == 'POST':
        data = {}
        form = VendorForm(request.POST, prefix='vend')
        if form.is_valid():
            data.update(form.cleaned_data)
        Vendor.objects.create(**data)
        return redirect('vendor')


def delete_vendor_view(request, pk):
    if request.method == 'POST':
        vendor = Vendor.objects.get(id=pk)
        vendor.delete()
        return redirect('vendor')


def get_vendor(request):
    if request.method == 'GET':
        vendor_id = request.GET.get('vendor_id')
        vendor = VendorSerializer(Vendor.objects.get(id=vendor_id))
        return JsonResponse(vendor.data)


def display_vendors_view(request):
    if request.method == 'GET':
        vendors = sort_ascending_descending(request, Vendor)
        state = FilterState.objects.get(name='Vendors_basic')
        column_list = change_column_position(request, state)
        myFilter = VendorFilter(request.GET, queryset=vendors)
        queryset = myFilter.qs
        number_of_objects = len(queryset)
        page_number = request.GET.get('page')
        print(number_of_objects)
        page_obj, dictionaries = paginate(queryset, myFilter, page_number)
        return render(request, 'vendor/vendor_contents.html', {'page_obj': page_obj,
                                                               'myFilter': myFilter,
                                                               'n_prod': number_of_objects,
                                                               'columns': column_list,
                                                               'dicts': dictionaries})

def update_vendor_view(request):
    if request.method == 'GET':
        pk = request.GET.get('pk')
        vendor = Vendor.objects.get(id=pk)
        data = vendor.__dict__
        vendor_form = VendorForm(initial=data)
        return render(request, 'vendor/update_vendor.html', {'vendor_form': vendor_form, 'requested_view_type': 'update','pk':pk})
    if request.method == 'POST':
        pk = request.POST.get('pk')
        print(pk)
        data = {}
        form = VendorForm(request.POST, prefix='vend')
        if form.is_valid():
            data.update(form.cleaned_data)
        print('Printing DATA:', data)
        Vendor.objects.filter(id=pk).update(**data)
        return redirect('vendor')
