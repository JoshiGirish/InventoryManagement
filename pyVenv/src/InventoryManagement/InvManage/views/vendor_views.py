from django.shortcuts import render
from django.shortcuts import redirect
from InvManage.forms import *
from InvManage.models import *
from InvManage.filters import VendorFilter
from django.http import JsonResponse
from InvManage.serializers import VendorSerializer
from InvManage.scripts.filters import *
from InvManage.scripts.helpers import create_event


def create_vendor_view(request):
    """ Creates the vendor creation view. """
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

def delete_vendor_view(request, pk):
    if request.method == 'POST':
        vendor = Vendor.objects.get(id=pk)
        create_event(vendor,'Deleted')
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
        page_obj, data = paginate(queryset, myFilter, page_number)
        print(data)
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
                                                               'dicts': dictionaries})

def update_vendor_view(request):
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
                                                address=add,
                                                communication=com,
                                                bankaccount=acc,
                                                purchasedata=pur
                                            )
        create_event(Vendor.objects.get(id=pk),'Updated')
        return redirect('vendor')