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


def create_company_view(request):
	if request.method == 'GET':
		company_form = CompanyForm()
		thumbnail_form = ThumbnailForm()
		shipping_form = ShippingAddressForm()
		return render(request, 'company/company.html', {'company_form': company_form,
												'thumbnail_form': thumbnail_form,
												'shipping_form': shipping_form})
	if request.method == 'POST':
		comp_data = {}
		ship_data = {}
		company_form = CompanyForm(request.POST,prefix=CompanyForm.prefix)
		thumbnail_form = ThumbnailForm(request.POST,prefix=ThumbnailForm.prefix)
		shipping_form = ShippingAddressForm(request.POST, prefix= ShippingAddressForm.prefix)
		if company_form.is_valid() and shipping_form.is_valid():
			comp_data.update(company_form.cleaned_data)
			ship_data.update(shipping_form.cleaned_data)
		shippigaddress = ShippingAddress.objects.create(**ship_data)
		comp_data.update({'shippingaddress': shippigaddress})
		uploaded_file = request.FILES['thumbnail-image']
		comp_data.update({'image':uploaded_file})
		Company.objects.create(**comp_data)
		return redirect('/company')

def update_company_view(request,pk):
	if request.method == 'GET':
		company = Company.objects.get(id=pk)
		data = company.__dict__
		company_form = CompanyForm(initial=data)
		ship = company.shippingaddress.__dict__
		shipping_form = ShippingAddressForm(initial=ship)
		thumbnail = company.image.name
		return render(request, 'company/update_company.html', {'company_form': company_form,
												'thumbnail': thumbnail,
												'shipping_form': shipping_form})
	if request.method == 'POST':
		comp_data = {}
		ship_data = {}
		company_form = CompanyForm(request.POST,prefix=CompanyForm.prefix)
		thumbnail_form = ThumbnailForm(request.POST,prefix=ThumbnailForm.prefix)
		shipping_form = ShippingAddressForm(request.POST, prefix= ShippingAddressForm.prefix)
		print(company_form.is_valid())
		print(shipping_form.is_valid())
		if company_form.is_valid():
			comp_data.update(company_form.cleaned_data)
			ship_data.update(shipping_form.cleaned_data)
		shippigaddress = ShippingAddress.objects.create(**ship_data)
		comp_data.update({'shippingaddress': shippigaddress})
		uploaded_file = request.FILES['thumbnail-image']
		comp_data.update({'image':uploaded_file})
		Company.objects.filter(id=pk).update(**comp_data)
		fs = FileSystemStorage()
		fs.save(uploaded_file.name,uploaded_file)
		return redirect('/companies')

def delete_company_view(request,pk):
	if request.method == 'POST':
		company = Company.objects.get(id=pk)
		company.delete()
		return redirect('/companies')

def display_companies_view(request):
	if request.method == 'GET':
		companies = Company.objects.all()
		myFilter = CompanyFilter(request.GET, queryset=companies)
		products = myFilter.qs
		number_of_companies = len(companies)
		paginator = Paginator(companies,15)
		page_number = request.GET.get('page')
		page_obj = paginator.get_page(page_number)
		return render(request, 'company/companies.html',{'page_obj':page_obj,'myFilter':myFilter, 'n_prod': number_of_companies})
