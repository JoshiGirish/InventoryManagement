from django.shortcuts import render
from django.shortcuts import redirect
from InvManage.forms import *
from django.forms.formsets import formset_factory
from InvManage.models import *
from django.core.files.storage import FileSystemStorage
import io,csv
from InvManage.filters import ProductFilter, VendorFilter, PurchaseOrderFilter, CompanyFilter
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.db import IntegrityError, transaction
from InvManage.serializers import VendorSerializer, PPEntrySerializer, PurchaseOrderSerializer, InvoiceSerializer, ProductSerializer
from InvManage.scripts.filters import *


def create_vendor_view(request):
	if request.method == 'GET':
		vendors = []
		for i,vend in enumerate(Vendor.objects.all()):
			vendors.append({'id':vend.id,'name':vend.name,'code':vend.identifier})
		vendor_form = VendorForm()	
		return render(request, 'vendor/create_vendor.html',{'vendor_form': vendor_form, 'vendors': vendors})
	if request.method == 'POST':
		data = {}
		form = VendorForm(request.POST, prefix = 'vend')
		if form.is_valid():
			data.update(form.cleaned_data)
		Vendor.objects.create(**data)
		return redirect('/vendors')

def delete_vendor_view(request, pk):
	if request.method == 'POST':
		vendor = Vendor.objects.get(id=pk)
		vendor.delete()
		return redirect('/vendors')

def get_vendor(request):
	if request.method == 'GET':
		vendor_id = request.GET.get('vendor_id')
		vendor = VendorSerializer(Vendor.objects.get(id=vendor_id))
		return JsonResponse(vendor.data)

def display_vendors_view(request):
	if request.method == 'GET':
		vendors = Vendor.objects.all()
		myFilter = VendorFilter(request.GET, queryset=vendors)
		vendors = myFilter.qs
		number_of_vendors = len(vendors)
		paginator = Paginator(vendors,15)
		page_number = request.GET.get('page')
		page_obj = paginator.get_page(page_number)
		return render(request, 'vendor/vendors.html',{'page_obj':page_obj,'myFilter':myFilter, 'n_prod': number_of_vendors})
	
def update_vendor_view(request,pk):
	if request.method == 'GET':
		vendor = Vendor.objects.get(id=pk)
		data = vendor.__dict__
		vendor_form = VendorForm(initial=data)
		return render(request, 'vendor/update_vendor.html',{'vendor_form': vendor_form})
	if request.method == 'POST':
		data = {}
		form = VendorForm(request.POST, prefix = 'vend')
		if form.is_valid():
			data.update(form.cleaned_data)
		print('Printing DATA:',data)
		Vendor.objects.filter(id=pk).update(**data)
		return redirect('/vendors')

