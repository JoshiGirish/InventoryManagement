from django.shortcuts import render
from django.shortcuts import redirect
from InvManage.forms import *
from InvManage.models import *
from InvManage.filters import VendorFilter
from django.http import JsonResponse
from InvManage.serializers import VendorSerializer
from InvManage.scripts.filters import *
from InvManage.scripts.helpers import create_event
from InvManage.scripts.helpers import generate_form_parameter_string
from django.http import HttpResponse, JsonResponse


def create_vendor_view(request):
    """ 
        Creates a vendor on ``POST`` request, and returns a vendor creation form on ``GET`` request. 

        .. http:get:: /vendor

            Gets the vendor creation form.

            **Example request**:

            .. sourcecode:: http

                GET /vendor/ HTTP/1.1
                Host: localhost:8000
                Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
            
    
            **Example response**:

            .. sourcecode:: http

                HTTP/1.1 200 OK
                Vary: Accept
                Content-Type: text/html; charset=utf-8

            :reqheader Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
            :statuscode 200: Vendor creation form received successfully.

        .. http:post:: /vendor

            Creates a vendor.

            **Example request**:

            .. sourcecode:: http

                POST /vendor/ HTTP/1.1
                Host: localhost:8000
                Content-Type: multipart/form-data;

            :form vend-name: ``Lug Vendor``

            :form vend-identifier: ``TBPN-02692``

            :form vend-gstin: ``89AAC254254F2``

            :form ship-title: ``AKATSUKI``

            :form ship-name: ``Kuame Burns``

            :form ship-phone: ``679 166-3127``

            :form ship-address: ``Nonummy Avenue``

            :form ship-city: ``Chung Cheong``

            :form ship-state: ``Guanacaste``

            :form ship-country: ``tellusidnunc.net``

            :form ship-website: ``Germany.protitor@tellusid.net``

            :form ship-post: ``8949``

            :form pdform-currency: ``DEM``

            :form pdform-minorder: ``2000``

            :form pdform-contactperson: ``Harding Gross``

            :form pdform-refcode: ``CUST000124``

            :form pdform-transportmode: ``Express``

            :form com-language: ``German``

            :form com-phone: ``936 651-4817``

            :form com-email: ``non.sollicitudin@uttincidunt.org``

            :form com-fax: ``323 555 1234``

            :form bank-name: ``FIRST FLORIDA INTEGRITY BANK``

            :form bank-branch: ``Bavaria``

            :form bank-region: ``Bayem``

            :form bank-route: ``67016325``

            :form bank-number: ``42543251393``

            :form bank-acctype: ``Current``

            :form bank-iban: ``DE6233542``

            :form bank-code: ``BA54354354``

            :form bank-branchcode: ``BA35435823``
            
            :resheader Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryLTR88aZAnBUSE7mv
            :statuscode 302: Redirects to ``/vendor``.

    """
    if request.method == 'GET':
        # Create a list of vendors
        vendors = []
        for i, vend in enumerate(Vendor.objects.all()):
            vendors.append(
                {'id': vend.id, 'name': vend.name, 'code': vend.identifier})
        return render(request, 'vendor.html', { 'vendor_form':      VendorForm(),
                                                'address_form':     ShippingAddressForm(),
                                                'com_form':         CommunicationForm(),
                                                'purchasing_form':  PurchaseDataForm(),
                                                'account_form':     BankAccountForm(),
                                                'vendors':          vendors,
                                                'requested_view_type': 'create'})
    if request.method == 'POST':
        data = {}
        vendor_form = VendorForm(request.POST, prefix='vend')
        address_form = ShippingAddressForm(request.POST, prefix='ship')
        com_form = CommunicationForm(request.POST, prefix='com')
        purchasing_form = PurchaseDataForm(request.POST, prefix='pdform')
        account_form = BankAccountForm(request.POST, prefix='bank')
        print(request.POST)
        if vendor_form.is_valid():
            data.update(vendor_form.cleaned_data)
        # Create address instance
        if address_form.is_valid():
            add = ShippingAddress.objects.create(**address_form.cleaned_data)
        # Create communication instance
        if com_form.is_valid():
            print(com_form.is_valid())
            com = Communication.objects.create(**com_form.cleaned_data)
        # Create purchase data instance
        if purchasing_form.is_valid():
            pur = PurchaseData.objects.create(**purchasing_form.cleaned_data)
        # Create account instance
        if account_form.is_valid():
            acc = BankAccount.objects.create(**account_form.cleaned_data)
       
        new_vendor = Vendor.objects.create( name=data['name'],
                                            identifier=data['identifier'],
                                            address=add,
                                            communication=com,
                                            bankaccount=acc,
                                            purchasedata=pur
                                            )
        create_event(new_vendor,'Created')
        return redirect('vendor')


def update_vendor_view(request):
    """ 
        Updates a vendor on ``POST`` request and returns the vendor update form for ``GET`` request. 

        .. http:get:: /vendor/update

            Gets the vendor update form whose primary key matches the query parameter ``pk``.

            **Example request**:

            .. sourcecode:: http

                GET /vendor/update HTTP/1.1
                Host: localhost:8000
                Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
            
            :query pk: The primary key of the vendor.
            
            **Example response**:

            .. sourcecode:: http

                HTTP/1.1 200 OK
                Vary: Accept
                Content-Type: text/html; charset=utf-8

            :reqheader Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
            :statuscode 200: Vendor update form received successfully.

        .. http:post:: /vendor/update

            Updates the vendor.

            **Example request**:

            .. sourcecode:: http

                POST /vendor/update HTTP/1.1
                Host: localhost:8000
                Content-Type: multipart/form-data;
    
            :form vend-name: ``Lug Vendor``

            :form vend-identifier: ``TBPN-02692``

            :form vend-gstin: ``89AAC254254F2``

            :form ship-title: ``AKATSUKI``

            :form ship-name: ``Kuame Burns``

            :form ship-phone: ``679 166-3127``

            :form ship-address: ``Nonummy Avenue``

            :form ship-city: ``Chung Cheong``

            :form ship-state: ``Guanacaste``

            :form ship-country: ``tellusidnunc.net``

            :form ship-website: ``Germany.protitor@tellusid.net``

            :form ship-post: ``8949``

            :form pdform-currency: ``DEM``

            :form pdform-minorder: ``1000``

            :form pdform-contactperson: ``Harding Gross``

            :form pdform-refcode: ``CUST000124``

            :form pdform-transportmode: ``Express``

            :form com-language: ``German``

            :form com-phone: ``936 651-4817``

            :form com-email: ``non.sollicitudin@uttincidunt.org``

            :form com-fax: ``323 555 1234``

            :form bank-name: ``FIRST FLORIDA INTEGRITY BANK``

            :form bank-branch: ``Bavaria``

            :form bank-region: ``Bayem``

            :form bank-route: ``67016325``

            :form bank-number: ``42543251393``

            :form bank-acctype: ``Current``

            :form bank-iban: ``DE6233542``

            :form bank-code: ``BA54354354``

            :form bank-branchcode: ``BA35435823``

            :resheader Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryLTR88aZAnBUSE7mv
            :statuscode 302: Redirects to ``/consumer``.

    """
    if request.method == 'GET':
        pk = request.GET.get('pk')
        vendor = Vendor.objects.get(id=pk)
        return render(request, 'vendor/update_vendor.html', {   'vendor_form':      VendorForm(initial=vendor.__dict__),
                                                                'address_form':     ShippingAddressForm(initial=vendor.address.__dict__),
                                                                'com_form':         CommunicationForm(initial=vendor.communication.__dict__),
                                                                'purchasing_form':  PurchaseDataForm(initial=vendor.purchasedata.__dict__),
                                                                'account_form':     BankAccountForm(initial=vendor.bankaccount.__dict__),
                                                                'requested_view_type': 'update',
                                                                'pk':pk
                                                            })
    if request.method == 'POST':
        pk = request.POST.get('pk')
        print(pk)
        data = {}
        vendor_form = VendorForm(request.POST, prefix='vend')
        address_form = ShippingAddressForm(request.POST, prefix='ship')
        com_form = CommunicationForm(request.POST, prefix='com')
        purchasing_form = PurchaseDataForm(request.POST, prefix='pdform')
        account_form = BankAccountForm(request.POST, prefix='bank')
        print(request.POST)
        if vendor_form.is_valid():
            data.update(vendor_form.cleaned_data)
        # Update address instance
        if address_form.is_valid():
            add = ShippingAddress.objects.create(**address_form.cleaned_data)
        # Update communication instance
        if com_form.is_valid():
            print(com_form.is_valid())
            com = Communication.objects.create(**com_form.cleaned_data)
        # Update purchase data instance
        if purchasing_form.is_valid():
            pur = PurchaseData.objects.create(**purchasing_form.cleaned_data)
        # Update account instance
        if account_form.is_valid():
            acc = BankAccount.objects.create(**account_form.cleaned_data)
       
        Vendor.objects.filter(id=pk).update(    name=data['name'],
                                                identifier=data['identifier'],
                                                gstin=data['gstin'],
                                                address=add,
                                                communication=com,
                                                bankaccount=acc,
                                                purchasedata=pur
                                            )
        create_event(Vendor.objects.get(id=pk),'Updated')
        return redirect('vendor')


def delete_vendor_view(request, pk):
    """ 
        Deletes the vendor with primary key ``pk`` on ``POST`` request.

        .. http:post:: /vendor/<str:object_id>/delete

            Deletes the vendor represented by the primary key ``object_id``.

            **Example request**:

            .. sourcecode:: http

                POST /vendor/5/delete HTTP/1.1
                Host: localhost:8000
                Content-Type: application/x-www-form-urlencoded
                
            :param object_id: Vendor primary key.
            :resheader Content-Type: application/x-www-form-urlencoded
            :statuscode 302: Redirects to ``/vendors``.
            :statuscode 500: Vendor matching query does not exist.

    """
    if request.method == 'POST':
        vendor = Vendor.objects.get(id=pk)
        create_event(vendor,'Deleted')
        vendor.delete()
        return redirect('vendor')


def display_vendors_view(request):
    """ 
        Retrieves the list of vendors on ``GET`` request.

        .. http:get:: /vendors/

            Gets the list of all vendors.

            **Example request**:

            .. sourcecode:: http

                GET /vendors/ HTTP/1.1
                Host: localhost:8000
                Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
            
            :form page: The page number of the vendors list.
    
            **Example response**:

            .. sourcecode:: http

                HTTP/1.1 200 OK
                Vary: Accept
                Content-Type: text/html; charset=utf-8

            :reqheader Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
            :statuscode 200: List of vendors received successfully.
    """
    if request.method == 'GET':
        vendors = Vendor.objects.all()
        state = FilterState.objects.get(name='Vendors_basic')
        column_list = change_column_position(request, state)
        myFilter = VendorFilter(request.GET, queryset=vendors)
        queryset = myFilter.qs
        number_of_objects = len(queryset)
        page_number = request.GET.get('page')
        page_obj, data = paginate(queryset, myFilter, page_number)
        dictionaries = []
        for obj in page_obj:
            objdata = { 'id': obj.pk,
                        'name': obj.name,
                        'identifier': obj.identifier,
                        'phone': obj.communication.phone,
                        'email': obj.communication.email,
                        'location': obj.address.city
                        }
            dictionaries.append(objdata)
        return render(request, 'vendor/vendor_contents.html', {'page_obj': page_obj,
                                                               'myFilter': myFilter,
                                                               'n_prod': number_of_objects,
                                                               'columns': column_list,
                                                               'dicts': dictionaries,
                                                               'url': request.build_absolute_uri('/vendors/')})
        

def get_vendor(request):
    """ 
        Returns the ``JSON`` serialized data of the requested vendor on ``GET`` request.

        .. http:get:: /get_vendor/

            Gets the JSON serialized data of the requested vendor.

            **Example request**:

            .. sourcecode:: http

                GET /get_vendor/ HTTP/1.1
                Host: localhost:8000
                Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
                
            :param vendor_id: Vendor primary key.
                
            **Example response**:

            .. sourcecode:: http

                HTTP/1.1 200 OK
                Vary: Accept
                Content-Type: application/json; charset=utf-8

                [
                    {
                        "name": "Lug Vendor",
                        "identifier": "TBPN-02692",
                        "gstin": "89AAC4683897343",
                        "address": {
                            "name": "Kuame Burns",
                            "address": "Nonummy Avenue",
                            "city": "Chung Cheong",
                            "phone": "679 166-3127",
                            "state": "Guanacaste",
                            "country": "tellusidnunc.net",
                            "post": "8949"
                        }
                    }
                ]

            :resheader Content-Type: application/json
            :statuscode 200: List of vendors received successfully.
            :statuscode 400: Bad request version
            :statuscode 500: Vendor matching query does not exist.
    """
    if request.method == 'GET':
        vendor_id = request.GET.get('vendor_id')
        vendor = VendorSerializer(Vendor.objects.get(id=vendor_id))
        return JsonResponse(vendor.data)