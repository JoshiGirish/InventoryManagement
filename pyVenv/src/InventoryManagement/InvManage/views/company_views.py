from django.shortcuts import render
from django.shortcuts import redirect
from InvManage.forms import *
from InvManage.models import *
from django.core.files.storage import FileSystemStorage
from InvManage.filters import CompanyFilter
from InvManage.scripts.filters import *
from InvManage.scripts.helpers import create_event
from django.urls import reverse


def create_company_view(request):
	if request.method == 'GET':
		company_form = CompanyForm()
		thumbnail_form = ThumbnailForm()
		shipping_form = ShippingAddressForm()
		return render(request, 'company/company.html', {'company_form': company_form,
												'thumbnail_form': thumbnail_form,
												'shipping_form': shipping_form,
												'requested_view_type': 'create'})		
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
		new_comp = Company.objects.create(**comp_data)
		create_event(new_comp,'Created')
		return redirect('company')

def update_company_view(request):
	if request.method == 'GET':
		pk = request.GET.get('pk')
		company = Company.objects.get(id=pk)
		data = company.__dict__
		company_form = CompanyForm(initial=data)
		ship = company.shippingaddress.__dict__
		shipping_form = ShippingAddressForm(initial=ship)
		thumbnail = company.image.name
		return render(request, 'company/update_company.html', {'company_form': company_form,
												'thumbnail': thumbnail,
												'shipping_form': shipping_form,
            									'requested_view_type':'update',
                     							'pk':pk	})
	if request.method == 'POST':
		pk = request.POST.get('pk')
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
		create_event(Company.objects.get(id=pk),'Updated')
		return redirect('company')

def delete_company_view(request,pk):
	if request.method == 'POST':
		company = Company.objects.get(id=pk)
		create_event(company,'Deleted')
		company.delete()
		return redirect('company')

def display_companies_view(request):
    if request.method == 'GET':
        companies = sort_ascending_descending(request, Company)
        state = FilterState.objects.get(name='Companies_basic')
        column_list = change_column_position(request, state)
        myFilter = CompanyFilter(request.GET, queryset=companies)
        queryset = myFilter.qs
        number_of_objects = len(queryset)
        page_number = request.GET.get('page')
        print(number_of_objects)
        page_obj, dictionaries = paginate(queryset, myFilter, page_number)
        return render(request, 'company/company_contents.html', {'page_obj': page_obj,
                                                               'myFilter': myFilter,
                                                               'n_prod': number_of_objects,
                                                               'columns': column_list,
                                                               'dicts': dictionaries,
                                                               'url': request.build_absolute_uri('/companies/')})
                                                            #    'url': request.get_host() + '/companies'})

		
	