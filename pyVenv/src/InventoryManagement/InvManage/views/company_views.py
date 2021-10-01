from django.shortcuts import render
from django.shortcuts import redirect
from InvManage.forms import *
from InvManage.models import *
from InvManage.serializers import CompanySerializer, ShippingAddressSerializer
from django.core.files.storage import FileSystemStorage
from InvManage.filters import CompanyFilter
from InvManage.scripts.filters import *
from InvManage.scripts.helpers import create_event
from django.urls import reverse
from drf_spectacular.utils import extend_schema
from drf_spectacular.types import OpenApiTypes
from rest_framework.renderers import JSONRenderer,HTMLFormRenderer
from rest_framework.decorators import api_view, renderer_classes


def create_company_view(request):
    """ 
        Creates a company on ``POST`` request and returns a company creation form  ``GET`` request. 

        .. http:get:: /company

            Gets the company creation form.

            **Example request**:

            .. sourcecode:: http

                GET /company/ HTTP/1.1
                Host: localhost:8000
                Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
            
    
            **Example response**:

            .. sourcecode:: http

                HTTP/1.1 200 OK
                Vary: Accept
                Content-Type: text/html; charset=utf-8

            :reqheader Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
            :statuscode 200: Company creation form received successfully.

        .. http:post:: /company

            Creates a company.

            **Example request**:

            .. sourcecode:: http

                POST /company/ HTTP/1.1
                Host: localhost:8000
                Content-Type: multipart/form-data;
    
            :form comp-name: ``Fringillami``

            :form comp-owner: ``Ivor Barnett``

            :form comp-gstin: ``89AAC056465468``

            :form comp-phone: ``332 220-7026``

            :form comp-address: ``Ap #849-6241 Euismod Av., 677598, Carinthia, Belgium``

            :form comp-email: ``est.tempor@fringillami.org``

            :form comp-location: ``Belgium``

            :form ship-title: ``FingDocks``

            :form ship-name: ``Harding Gross``

            :form ship-phone: ``936 651-4847``

            :form ship-address: ``8798 At, St., 7639``

            :form ship-city: ``Rome``

            :form ship-state: ``Lazio``

            :form ship-country: ``Italy``

            :form ship-website: ``fringdocs.com``

            :form ship-post: ``300326``

            :resheader Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryLTR88aZAnBUSE7mv
            :statuscode 302: Redirects to ``/company``.

    """
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
    """ 
        Updates a company on ``POST`` request and returns the company update form  ``GET`` request. 

        .. http:get:: /company/update

            Gets the company update form whose primary key matches the query parameter ``pk``.

            **Example request**:

            .. sourcecode:: http

                GET /company/update HTTP/1.1
                Host: localhost:8000
                Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
            
            :query pk: The primary key of the company.
            
            **Example response**:

            .. sourcecode:: http

                HTTP/1.1 200 OK
                Vary: Accept
                Content-Type: text/html; charset=utf-8

            :reqheader Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
            :statuscode 200: Company update form received successfully.

        .. http:post:: /company/update

            Updates a company.

            **Example request**:

            .. sourcecode:: http

                POST /company/ HTTP/1.1
                Host: localhost:8000
                Content-Type: multipart/form-data;
    
            :form pk: ``4``
    
            :form comp-name: ``Fringillami``

            :form comp-owner: ``Ivor Barnett``

            :form comp-gstin: ``89AAC056465468``

            :form comp-phone: ``332 220-7026``

            :form comp-address: ``Ap #849-6241 Euismod Av., 677598, Carinthia, Belgium``

            :form comp-email: ``est.tempor@fringillami.org``

            :form comp-location: ``Belgium``

            :form ship-title: ``FingDocks``

            :form ship-name: ``Harding Gross``

            :form ship-phone: ``936 651-4847``

            :form ship-address: ``8798 At, St., 7639``

            :form ship-city: ``Rome``

            :form ship-state: ``Lazio``

            :form ship-country: ``Italy``

            :form ship-website: ``fringdocs.com``

            :form ship-post: ``300326``

            :resheader Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryLTR88aZAnBUSE7mv
            :statuscode 302: Redirects to ``/company``.

    """
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
                                                'requested_view_type':'update','pk':pk	})
    if request.method == 'PUT':
        pk = request.PUT.get('pk')
        comp_data = {}
        ship_data = {}
        company_form = CompanyForm(request.PUT,prefix=CompanyForm.prefix)
        thumbnail_form = ThumbnailForm(request.PUT,prefix=ThumbnailForm.prefix)
        shipping_form = ShippingAddressForm(request.PUT, prefix= ShippingAddressForm.prefix)
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
    """ 
        Deletes the company with primary key ``pk`` on ``POST`` request.

        .. http:post:: /company/<str:object_id>/delete

            Deletes the company represented by the primary key ``object_id``.

            **Example request**:

            .. sourcecode:: http

                POST /company/32/delete HTTP/1.1
                Host: localhost:8000
                Content-Type: application/x-www-form-urlencoded
                
            :param object_id: Company primary key.
            :resheader Content-Type: application/x-www-form-urlencoded
            :statuscode 302: Redirects to ``/company``.
            :statuscode 500: Company matching query does not exist.

    """
    if request.method == 'POST':
        company = Company.objects.get(id=pk)
        create_event(company,'Deleted')
        company.delete()
        return redirect('company')

def display_companies_view(request):
    """ 
        Retrieves the list of companies on ``GET`` request.

        .. http:get:: /companies/

            Gets the list of all companies.

            **Example request**:

            .. sourcecode:: http

                GET /companies/ HTTP/1.1
                Host: localhost:8000
                Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
            
            :form page: The page number of the companies list.
    
            **Example response**:

            .. sourcecode:: http

                HTTP/1.1 200 OK
                Vary: Accept
                Content-Type: text/html; charset=utf-8

            :reqheader Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
            :statuscode 200: List of companies received successfully.
    """
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

        
    