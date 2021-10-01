from django.shortcuts import render
from django.shortcuts import redirect
from InvManage.forms import *
from django.forms.formsets import formset_factory
from InvManage.models import *
from InvManage.filters import PurchaseOrderFilter
from django.http import JsonResponse
from InvManage.serializers import ProductSerializer, PPEntrySerializer, PurchaseInvoiceSerializer
from InvManage.scripts.filters import *
from InvManage.scripts.helpers import create_event,get_parameter_list_from_request
import json


def create_purchase_order_view(request):
    """ 
        Creates a purchase order (PO) on ``POST`` request, and returns a PO creation form on ``GET`` request. 

        .. http:get:: /purchase_order

            Gets the purchase order creation form.

            **Example request**:

            .. sourcecode:: http

                GET /purchase_order/ HTTP/1.1
                Host: localhost:8000
                Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
            
    
            **Example response**:

            .. sourcecode:: http

                HTTP/1.1 200 OK
                Vary: Accept
                Content-Type: text/html; charset=utf-8

            :reqheader Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
            :statuscode 200: Purchase order creation form received successfully.

        .. http:post:: /purchase_order

            Creates a purchase order.

            **Example request**:

            .. sourcecode:: http

                POST /purchase_order/ HTTP/1.1
                Host: localhost:8000
                Content-Type: multipart/form-data;

            :form po-vendor: ``4``

            :form vend-name: ``Girish``

            :form vend-identifier: ``GJ``

            :form po-po: ``69``

            :form po-date: ``2021-09-29``

            :form po-tax: ``12``

            :form po-discount: ``8``

            :form po-paid: ``4500``

            :form po-balance: ``1200``

            :form ship-title: ``FingDocks``

            :form ship-name: ``Harding Gross``

            :form ship-phone: ``936 651-4847``

            :form ship-address: ``8798 At, St., 7639``

            :form ship-city: ``Rome``

            :form ship-state: ``Lazio``

            :form ship-country: ``Italy``

            :form ship-website: ``http://fringdocs.com``

            :form ship-post: ``300326``

            :form po-subtotal: ``2595000.00``

            :form po-taxtotal: ``207600.00``

            :form po-ordertotal: ``2802600.00``

            :form form-TOTAL_FORMS: ``2``

            :form form-INITIAL_FORMS: ``0``

            :form form-MIN_NUM_FORMS: ````

            :form form-MAX_NUM_FORMS: ````

            :form form-0-product: ``649``

            :form form-0-quantity: ``300``

            :form form-0-price: ``4500``

            :form form-0-discount: ``10``

            :form form-0-DELETE: ````

            :form form-0-ppe_id: ``-1``

            :form form-1-product: ``664``

            :form form-1-quantity: ``250``

            :form form-1-price: ``6000``

            :form form-1-discount: ``8``

            :form form-1-DELETE: ````

            :form form-1-ppe_id: ``-1``
                        
            :resheader Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryLTR88aZAnBUSE7mv
            :statuscode 302: Redirects to ``/purchase_order``.

    """
    ProductPurchaseEntryFormset = formset_factory(ProductPurchaseEntryForm)
    data = {
        'form-TOTAL_FORMS': '0',
        'form-INITIAL_FORMS': '0',
        'form-MAX_NUM_FORMS': '',
    }
    pentry_formset = ProductPurchaseEntryFormset(data)
    pentry_form = ProductPurchaseEntryForm()
    shipping_form = ShippingAddressForm()
    company = Company.objects.all().last()
    ship_data = company.shippingaddress.__dict__
    if request.method == 'GET':
        shipping_form = ShippingAddressForm(initial=ship_data)
        purchase_form = PurchaseOrderBasicInfo()
        vendor_form = VendorForm()
        prods = []
        for i, prod in enumerate(Product.objects.all()):
            prods.append({'id': prod.id, 'name': prod.name,
                          'code': prod.identifier})
        vendors = []
        for i, vend in enumerate(Vendor.objects.all()):
            vendors.append({'id': vend.id, 'name': vend.name})
        context = {
            'purchase_form': purchase_form,
            'pentry_form': pentry_form,
            'prods': prods,
            'vendors': vendors,
            'vendor_form': vendor_form,
            'pentry_formset': pentry_formset,
            'ppes': {},
            'shipping_form': shipping_form,
            'requested_view_type': 'create',
        }
        return render(request, 'purchase_order.html', context)
    if request.method == 'POST':
        print(request.POST)
        ProductPurchaseEntryFormset = formset_factory(
            ProductPurchaseEntryForm, can_delete=True)
        purchase_form = PurchaseOrderBasicInfo(request.POST, prefix='po')
        pentry_formset = ProductPurchaseEntryFormset(
            request.POST, prefix='form')
        data = {}
        print(purchase_form.is_valid())
        print(pentry_formset.is_valid())
        print(pentry_formset.errors)
        if purchase_form.is_valid():
            vendor = purchase_form.cleaned_data.get('vendor')
            po = purchase_form.cleaned_data.get('po')
            date = purchase_form.cleaned_data.get('date')
            tax = purchase_form.cleaned_data.get('tax')
            discount = purchase_form.cleaned_data.get('discount')
            paid = purchase_form.cleaned_data.get('paid')
            balance = purchase_form.cleaned_data.get('balance')
            subtotal = purchase_form.cleaned_data.get('subtotal')
            taxtotal = purchase_form.cleaned_data.get('taxtotal')
            ordertotal = purchase_form.cleaned_data.get('ordertotal')
            data = {
                'vendor': vendor,
                'po': po,
                'date': date,
                'tax': tax,
                'discount': discount,
                'paid': paid,
                'balance': balance,
                'subtotal': subtotal,
                'taxtotal': taxtotal,
                'ordertotal': ordertotal
            }
            new_po = PurchaseOrder.objects.create(**data)
            for ppeform in pentry_formset:
                if ppeform.is_valid():
                    ppe_id = ppeform.cleaned_data.get('ppe_id')
                    product = ppeform.cleaned_data.get('product')
                    quantity = ppeform.cleaned_data.get('quantity')
                    price = ppeform.cleaned_data.get('price')
                    discount = ppeform.cleaned_data.get('discount')
                    order = PurchaseOrder.objects.get(id=new_po.pk)
                    print(ppe_id)
                    validated_data = {'ppe_id': ppe_id,
                                      'product': ProductSerializer(product).data,
                                      'quantity': quantity,
                                      'price': price,
                                      'discount': discount,
                                      'order': new_po.pk,
                                      }
                    if ppe_id == -1:  # new ppe to be created if id is -1
                        pentry = PPEntrySerializer(data=validated_data)
                        if pentry.is_valid():
                            pentry.save()
                        else:
                            print(pentry.errors)
        create_event(new_po,'Created')
        return redirect('purchase_order')


def update_purchase_order_view(request):
    """ 
        Updates a purchase order on ``POST`` request and returns the purchase order update form for ``GET`` request. 

        .. http:get:: /purchaes_order/update

            Gets the purchase order update form whose primary key matches the query parameter ``pk``.

            **Example request**:

            .. sourcecode:: http

                GET /purchase_order/update HTTP/1.1
                Host: localhost:8000
                Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
            
            :query pk: The primary key of the purchase order.
            
            **Example response**:

            .. sourcecode:: http

                HTTP/1.1 200 OK
                Vary: Accept
                Content-Type: text/html; charset=utf-8

            :reqheader Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
            :statuscode 200: Purchase order update form received successfully.

        .. http:post:: /purchase_order/update

            Updates the purchase order.

            **Example request**:

            .. sourcecode:: http

                POST /purchase_order/update HTTP/1.1
                Host: localhost:8000
                Content-Type: multipart/form-data;
    
            :form pk: ``187``

            :form po-vendor: ``4``

            :form vend-name: ``Girish``

            :form vend-identifier: ``GJ``

            :form po-po: ``69``

            :form po-date: ``2021-09-29``

            :form po-tax: ``12``

            :form po-discount: ``8.0``

            :form po-paid: ``4500.0``

            :form po-balance: ``1200.0``

            :form ship-title: ``FingDocks``

            :form ship-name: ``Harding Gross``

            :form ship-phone: ``936 651-4847``

            :form ship-address: ``8798 At, St., 7639``

            :form ship-city: ``Rome``

            :form ship-state: ``Lazio``

            :form ship-country: ``Italy``

            :form ship-website: ``http://fringdocs.com``

            :form ship-post: ``300326``

            :form po-subtotal: ``2595000.0``

            :form po-taxtotal: ``207600.0``

            :form po-ordertotal: ``2802600.0``

            :form form-TOTAL_FORMS: ``2``

            :form form-INITIAL_FORMS: ``2``

            :form form-MIN_NUM_FORMS: ````

            :form form-MAX_NUM_FORMS: ````

            :form form-0-product: ``649``

            :form form-0-quantity: ``300``

            :form form-0-price: ``4500``

            :form form-0-discount: ``10``

            :form form-0-DELETE: ````

            :form form-0-ppe_id: ``339``

            :form form-1-product: ``664``

            :form form-1-quantity: ``250``

            :form form-1-price: ``6000``

            :form form-1-discount: ``8``

            :form form-1-DELETE: ````

            :form form-1-ppe_id: ``340``

            :resheader Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryLTR88aZAnBUSE7mv
            :statuscode 302: Redirects to ``/consumer``.

    """
    if request.method == 'GET':
        pk = request.GET.get('pk')
        print(pk)
        po = PurchaseOrder.objects.get(id=pk)
        po_data = po.__dict__
        vendor = po.vendor
        ven_data = vendor.__dict__
        company = Company.objects.all().last()
        ship_data = company.shippingaddress.__dict__
        ProductPurchaseEntryFormset = formset_factory(
            ProductPurchaseEntryForm, can_delete=True)
        ppes = PurchaseOrder.objects.get(id=pk).productpurchaseentry_set.all()
        ppes_serialized = []
        for ppe in ppes:
            d = PPEntrySerializer(ppe)
            ppes_serialized.append(d.data)
        data = {
            'form-TOTAL_FORMS': len(ppes),
            'form-INITIAL_FORMS': len(ppes),
            'form-MAX_NUM_FORMS': '',
        }
        print(ppes_serialized)
        pentry_formset = ProductPurchaseEntryFormset(data, initial=ppes)
        pentry_form = ProductPurchaseEntryForm()
        purchase_form = PurchaseOrderBasicInfo(initial=po_data)
        # print(purchase_form)
        vendor_form = VendorForm(initial=ven_data)
        shipping_form = ShippingAddressForm(initial=ship_data)
        prods = []
        for i, prod in enumerate(Product.objects.all()):
            prods.append({'id': prod.id, 'name': prod.name,
                          'code': prod.identifier})
        vendors = []
        for i, vend in enumerate(Vendor.objects.all()):
            vendors.append({'id': vend.id, 'name': vend.name})
        context = {
            'purchase_form': purchase_form,
            'pentry_form': pentry_form,
            'prods': prods,
            'vendor_id': vendor.pk,
            'vendors': vendors,
            'vendor_form': vendor_form,
            'pentry_formset': pentry_formset,
            'ppes': ppes_serialized,
            'shipping_form': shipping_form,
            'requested_view_type': 'update',
            'pk': pk,
        }
        return render(request, 'purchase_order/update_purchase_order.html', context)
    if request.method == 'POST':
        pk = request.POST.get('pk')
        print(pk)
        ProductPurchaseEntryFormset = formset_factory(
            ProductPurchaseEntryForm, can_delete=True)
        purchase_form = PurchaseOrderBasicInfo(request.POST, prefix='po')
        pentry_formset = ProductPurchaseEntryFormset(
            request.POST, prefix='form')
        data = {}
        print(purchase_form.is_valid())
        print(pentry_formset.is_valid())
        if purchase_form.is_valid():
            vendor = purchase_form.cleaned_data.get('vendor')
            po = purchase_form.cleaned_data.get('po')
            date = purchase_form.cleaned_data.get('date')
            tax = purchase_form.cleaned_data.get('tax')
            discount = purchase_form.cleaned_data.get('discount')
            paid = purchase_form.cleaned_data.get('paid')
            balance = purchase_form.cleaned_data.get('balance')
            subtotal = purchase_form.cleaned_data.get('subtotal')
            taxtotal = purchase_form.cleaned_data.get('taxtotal')
            ordertotal = purchase_form.cleaned_data.get('ordertotal')
            data = {
                'vendor': vendor,
                'po': po,
                'date': date,
                'tax': tax,
                'discount': discount,
                'paid': paid,
                'balance': balance,
                'subtotal': subtotal,
                'taxtotal': taxtotal,
                'ordertotal': ordertotal
            }
            PurchaseOrder.objects.filter(id=pk).update(**data)
            for ppeform in pentry_formset:
                if ppeform.is_valid():
                    ppe_id = ppeform.cleaned_data.get('ppe_id')
                    product = ppeform.cleaned_data.get('product')
                    quantity = ppeform.cleaned_data.get('quantity')
                    price = ppeform.cleaned_data.get('price')
                    discount = ppeform.cleaned_data.get('discount')
                    order = PurchaseOrder.objects.get(id=pk)
                    print(ppe_id)
                    validated_data = {'ppe_id': ppe_id,
                                    #   'product': product.__dict__,
                                      'product': ProductSerializer(product).data,
                                      'quantity': quantity,
                                      'price': price,
                                      'discount': discount,
                                      'order': pk,
                                      }
                    if ppe_id == -1:  # new ppe to be created if id is -1
                        pentry = PPEntrySerializer(data=validated_data)
                        if pentry.is_valid():
                            pentry.save()
                            product.quantity += quantity  # Add the quantity to the product stock as it is new ppe
                        else:
                            print(pentry.errors)
                    else:
                        ppe = ProductPurchaseEntry.objects.get(id=ppe_id)
                        old_quantity = ppe.quantity
                        pentry = PPEntrySerializer(ppe, data=validated_data)
                        if pentry.is_valid():
                            pentry.save()
                            product.quantity += quantity-old_quantity
                            product.save()  # Save the changes to the product instance
                        else:
                            print(pentry.errors)
            for ppeform in pentry_formset.deleted_forms:
                print(ppeform.is_valid())
                ppe_id = ppeform.cleaned_data.get('ppe_id')
                print(ppe_id)
                product = ppeform.cleaned_data.get('product')
                quantity = ppeform.cleaned_data.get('quantity')
                if ppe_id != -1:
                    ppe = ProductPurchaseEntry.objects.get(id=ppe_id)
                    product.quantity -= quantity
                    ppe.delete()
        create_event(PurchaseOrder.objects.get(id=pk),'Updated')
        # return redirect('purchase_order')
        return HttpResponse(f'<p>{generate_form_parameter_string(request.POST)}</p>')


def display_purchase_orders_view(request):
    """ 
        Retrieves the list of purchase orders on ``GET`` request.

        .. http:get:: /purchase_orders/

            Gets the list of all purchase orders.

            **Example request**:

            .. sourcecode:: http

                GET /purchase_orders/ HTTP/1.1
                Host: localhost:8000
                Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
            
            :form page: The page number of the purchase order list.
    
            **Example response**:

            .. sourcecode:: http

                HTTP/1.1 200 OK
                Vary: Accept
                Content-Type: text/html; charset=utf-8

            :reqheader Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
            :statuscode 200: List of purchase orders received successfully.
    """
    if request.method == 'GET':
        exclude_ids = get_parameter_list_from_request(request,'exclude')
        vendor_names = get_parameter_list_from_request(request,'vendor_names')
        pos = PurchaseOrder.objects.all().exclude(pk__in=exclude_ids)
        state = FilterState.objects.get(name='POs_basic')
        column_list = change_column_position(request, state)
        myFilter = PurchaseOrderFilter(request.GET, queryset=pos)
        queryset = myFilter.qs
        number_of_objects = len(queryset)
        page_number = request.GET.get('page')
        page_obj, dictionaries = paginate(queryset, myFilter, page_number)
        # dictionary contains only vendor id and not vendor name. So add it.
        for dictionary in dictionaries:
            dictionary['status'] = PurchaseOrder.objects.get(id=dictionary['id']).is_complete()
            vend_id = dictionary['vendor_id']
            vendor = Vendor.objects.get(id=vend_id)
            dictionary['vendor'] = vendor.name
        print(dictionaries)
        if request.GET.get('form') == 'objectFilterForm' or request.GET.get('form') == None:
            return render(request, 'purchase_order/purchase_order_contents.html', {'page_obj': page_obj,
                                                                               'myFilter': myFilter,
                                                                               'n_prod': number_of_objects,
                                                                               'columns': column_list,
                                                                               'dicts': dictionaries,
                                                                               'url': request.build_absolute_uri('/purchase_orders/')})
        elif request.GET.get('form') == 'selectionFilterForm':
            return render(request, 'reuse/selection_dialog_box/table.html', {'page_obj': page_obj,
                                                                               'myFilter': myFilter,
                                                                               'n_prod': number_of_objects,
                                                                               'columns': column_list,
                                                                               'dicts': dictionaries,
                                                                               'url': request.build_absolute_uri('/purchase_orders/')})
            
def delete_purchase_order_view(request, pk):
    """ 
        Deletes the purchase order with primary key ``object_id`` on ``POST`` request.

        .. http:post:: /purchase_order/<str:object_id>/delete

            Deletes the consumer represented by the primary key ``object_id``.

            **Example request**:

            .. sourcecode:: http

                POST /purchase_order/187/delete HTTP/1.1
                Host: localhost:8000
                Content-Type: application/x-www-form-urlencoded
                
            :param object_id: Purchase order primary key.
            :resheader Content-Type: application/x-www-form-urlencoded
            :statuscode 302: Redirects to ``/purchase_order``.
            :statuscode 500: Purchase order matching query does not exist.

    """
    if request.method == 'POST':
        po = PurchaseOrder.objects.get(id=pk)
        create_event(po,'Deleted')
        po.delete()
        return redirect('purchase_order')
    

def print_purchase_order_view(request, pk):
    """ 
        Opens the purchase order with primary key ``po_id`` for printing on ``GET`` request.

        .. http:post:: /purchase_order/<str:po_id>/print

            Opens the purchase order represented by the primary key ``po_id``.

            **Example request**:

            .. sourcecode:: http

                POST /purchase_order/182/print HTTP/1.1
                Host: localhost:8000
                Content-Type: application/x-www-form-urlencoded
                
            **Example response**:

            .. sourcecode:: http

                HTTP/1.1 200 OK
                Vary: Accept
                Content-Type: application/json; charset=utf-8
                
                [
                    {
                        "company": {
                            "name": "Fringillami",
                            "owner": "Ivor Barnett",
                            "gstin": "89AAC056465468",
                            "phone": "332 220-7026",
                            "address": "Ap #849-6241 Euismod Av., 677598, Carinthia, Belgium",
                            "email": "est.tempor@fringillami.org",
                            "location": "Belgium",
                            "image": "/media/images/hyperlink-green_x91WW5n.png"
                        },
                        "po": {
                            "vendor": {
                                "name": "Girish",
                                "identifier": "GJ",
                                "gstin": "GSTIN002",
                                "address": {
                                    "name": "alsf",
                                    "address": "jas;k",
                                    "city": ";sdalkf",
                                    "phone": "alsf",
                                    "state": "kjdflk",
                                    "country": "ljflkj",
                                    "post": "54545"
                                }
                            },
                            "date": "25-Sep-2021",
                            "po": 293,
                            "subtotal": 279975.0,
                            "taxtotal": 22398.0,
                            "ordertotal": 302373.0,
                            "ppes": [
                                {
                                    "ppe_id": 324,
                                    "product": {
                                        "pk": 637,
                                        "name": "piano",
                                        "category": "Ultricies PC",
                                        "quantity": 23921,
                                        "identifier": "PROD9",
                                        "location": "Musselburgh",
                                        "description": "88-key, Tri-sensor Scaled Hammer Action Keyboard II, Simulated ebony and ivory keys ",
                                        "prod_id": 637
                                    },
                                    "quantity": 100,
                                    "price": 10.0,
                                    "discount": 0.0,
                                    "order": 182,
                                    "pendingQty": 50
                                },
                                {
                                    "ppe_id": 325,
                                    "product": {
                                        "pk": 645,
                                        "name": "Tabl",
                                        "category": "Sociis Natoque Company",
                                        "quantity": 38276,
                                        "identifier": "PROD17",
                                        "location": "Schagen",
                                        "description": "aldgjlakjlkasdj",
                                        "prod_id": 645
                                    },
                                    "quantity": 250,
                                    "price": 90.0,
                                    "discount": 8.0,
                                    "order": 182,
                                    "pendingQty": 70
                                },
                                {
                                    "ppe_id": 326,
                                    "product": {
                                        "pk": 638,
                                        "name": "Goblet drum",
                                        "category": "Est Congue Consulting",
                                        "quantity": 46076,
                                        "identifier": "PROD10",
                                        "location": "Kaluga",
                                        "description": "aldgjlakjlkasdj",
                                        "prod_id": 638
                                    },
                                    "quantity": 200,
                                    "price": 150.0,
                                    "discount": 12.0,
                                    "order": 182,
                                    "pendingQty": 200
                                },
                                {
                                    "ppe_id": 327,
                                    "product": {
                                        "pk": 643,
                                        "name": "quinto",
                                        "category": "Enim Suspendisse Associates",
                                        "quantity": 51099,
                                        "identifier": "PROD15",
                                        "location": "Nagpur",
                                        "description": "aldgjlakjlkasdj",
                                        "prod_id": 643
                                    },
                                    "quantity": 350,
                                    "price": 150.0,
                                    "discount": 10.0,
                                    "order": 182,
                                    "pendingQty": 350
                                },
                                {
                                    "ppe_id": 328,
                                    "product": {
                                        "pk": 651,
                                        "name": "Igihumurizo",
                                        "category": "Curabitur Massa Vestibulum Consulting",
                                        "quantity": 48553,
                                        "identifier": "PROD23",
                                        "location": "Yeovil",
                                        "description": "aldgjlakjlkasdj",
                                        "prod_id": 651
                                    },
                                    "quantity": 500,
                                    "price": 50.0,
                                    "discount": 6.0,
                                    "order": 182,
                                    "pendingQty": 500
                                },
                                {
                                    "ppe_id": 329,
                                    "product": {
                                        "pk": 653,
                                        "name": "Balsié",
                                        "category": "Eu Foundation",
                                        "quantity": 29988,
                                        "identifier": "PROD25",
                                        "location": "Sudbury",
                                        "description": "aldgjlakjlkasdj",
                                        "prod_id": 653
                                    },
                                    "quantity": 200,
                                    "price": 500.0,
                                    "discount": 15.0,
                                    "order": 182,
                                    "pendingQty": 200
                                },
                                {
                                    "ppe_id": 330,
                                    "product": {
                                        "pk": 656,
                                        "name": "Padayani thappu",
                                        "category": "Posuere LLP",
                                        "quantity": 6358,
                                        "identifier": "PROD28",
                                        "location": "Ruvo del Monte",
                                        "description": "aldgjlakjlkasdj",
                                        "prod_id": 656
                                    },
                                    "quantity": 350,
                                    "price": 250.0,
                                    "discount": 13.0,
                                    "order": 182,
                                    "pendingQty": 350
                                }
                            ]
                        },
                        "shippingaddress": {
                            "name": "Harding Gross",
                            "address": "8798 At, St., 7639",
                            "city": "Rome",
                            "phone": "936 651-4847",
                            "state": "Lazio",
                            "country": "Italy",
                            "post": "300326"
                        },
                        "communication": {
                            "email": "asfs@aflk.com",
                            "phone": "6546432"
                        }
                    }
                ]
            
            :param po_id: Purchase order primary key.
            :resheader Content-Type: application/json
            :statuscode 200: Purchase order print request successful.
            :statuscode 500: Purchase order matching query does not exist.

    """

    if request.method == 'GET':
        po = PurchaseOrder.objects.get(id=pk)
        company = Company.objects.all().last()
        company_shippingaddress = company.shippingaddress
        vendor_communication = po.vendor.communication
        invoice_serializer = PurchaseInvoiceSerializer(
            PurchaseInvoice(company=company, 
                            po=po, 
                            shippingaddress=company_shippingaddress, 
                            communication=vendor_communication))
        print(JsonResponse(invoice_serializer.data))
    return JsonResponse(invoice_serializer.data)


def get_product_purchase_entries_view(request):
    """ 
        Returns the ``JSON`` serialized data of product purchase entries on ``GET`` request.

        .. http:get:: /product_purchase_entries/

            Gets the JSON serialized data of the requested product purchase entries.

            **Example request**:

            .. sourcecode:: http

                GET /product_purchase_entries/ HTTP/1.1
                Host: localhost:8000
                Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
                
            **Example response**:

            .. sourcecode:: http

                HTTP/1.1 200 OK
                Vary: Accept
                Content-Type: application/json; charset=utf-8

                [
                    {
                        "ppe_id": 324,
                        "product": {
                            "pk": 637,
                            "name": "piano",
                            "category": "Ultricies PC",
                            "quantity": 23921,
                            "identifier": "PROD9",
                            "location": "Musselburgh",
                            "description": "88-key, Tri-sensor Scaled Hammer Action Keyboard II, Simulated ebony and ivory keys ",
                            "prod_id": 637
                        },
                        "quantity": 100,
                        "price": 10.0,
                        "discount": 0.0,
                        "order": 182,
                        "pendingQty": 50,
                        "po": 293
                    },
                    {
                        "ppe_id": 325,
                        "product": {
                            "pk": 645,
                            "name": "Tabl",
                            "category": "Sociis Natoque Company",
                            "quantity": 38276,
                            "identifier": "PROD17",
                            "location": "Schagen",
                            "description": "aldgjlakjlkasdj",
                            "prod_id": 645
                        },
                        "quantity": 250,
                        "price": 90.0,
                        "discount": 8.0,
                        "order": 182,
                        "pendingQty": 70,
                        "po": 293
                    },
                    {
                        "ppe_id": 326,
                        "product": {
                            "pk": 638,
                            "name": "Goblet drum",
                            "category": "Est Congue Consulting",
                            "quantity": 46076,
                            "identifier": "PROD10",
                            "location": "Kaluga",
                            "description": "aldgjlakjlkasdj",
                            "prod_id": 638
                        },
                        "quantity": 200,
                        "price": 150.0,
                        "discount": 12.0,
                        "order": 182,
                        "pendingQty": 200,
                        "po": 293
                    },
                    {
                        "ppe_id": 327,
                        "product": {
                            "pk": 643,
                            "name": "quinto",
                            "category": "Enim Suspendisse Associates",
                            "quantity": 51099,
                            "identifier": "PROD15",
                            "location": "Nagpur",
                            "description": "aldgjlakjlkasdj",
                            "prod_id": 643
                        },
                        "quantity": 350,
                        "price": 150.0,
                        "discount": 10.0,
                        "order": 182,
                        "pendingQty": 350,
                        "po": 293
                    },
                    {
                        "ppe_id": 328,
                        "product": {
                            "pk": 651,
                            "name": "Igihumurizo",
                            "category": "Curabitur Massa Vestibulum Consulting",
                            "quantity": 48553,
                            "identifier": "PROD23",
                            "location": "Yeovil",
                            "description": "aldgjlakjlkasdj",
                            "prod_id": 651
                        },
                        "quantity": 500,
                        "price": 50.0,
                        "discount": 6.0,
                        "order": 182,
                        "pendingQty": 500,
                        "po": 293
                    },
                    {
                        "ppe_id": 329,
                        "product": {
                            "pk": 653,
                            "name": "Balsié",
                            "category": "Eu Foundation",
                            "quantity": 29988,
                            "identifier": "PROD25",
                            "location": "Sudbury",
                            "description": "aldgjlakjlkasdj",
                            "prod_id": 653
                        },
                        "quantity": 200,
                        "price": 500.0,
                        "discount": 15.0,
                        "order": 182,
                        "pendingQty": 200,
                        "po": 293
                    },
                    {
                        "ppe_id": 330,
                        "product": {
                            "pk": 656,
                            "name": "Padayani thappu",
                            "category": "Posuere LLP",
                            "quantity": 6358,
                            "identifier": "PROD28",
                            "location": "Ruvo del Monte",
                            "description": "aldgjlakjlkasdj",
                            "prod_id": 656
                        },
                        "quantity": 350,
                        "price": 250.0,
                        "discount": 13.0,
                        "order": 182,
                        "pendingQty": 350,
                        "po": 293
                    }
                ]

            :reqheader Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
            :statuscode 200: List of product purchase entries received successfully.
            :statuscode 400: Bad request version
            :statuscode 500: Product purchase entries matching query does not exist.
    """
    if request.method == 'GET':
        pks = request.GET.getlist('pks[]')
        ppes = []
        for pk in pks:
            ppes.extend(PurchaseOrder.objects.get(id=int(pk)).productpurchaseentry_set.all())
        ppes_serialized = []
        for ppe in ppes:
            d = PPEntrySerializer(ppe)
            ppes_serialized.append({**d.data,**{'po':ppe.order.po}})
    return JsonResponse(ppes_serialized, safe=False)