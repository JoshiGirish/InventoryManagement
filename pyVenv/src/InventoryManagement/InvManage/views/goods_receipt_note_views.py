from django.shortcuts import render
from django.shortcuts import redirect
from InvManage.forms import *
from django.forms.formsets import formset_factory
from InvManage.models import *
from InvManage.filters import GoodsReceiptNoteFilter
from django.http import JsonResponse
from InvManage.serializers import GRNEntrySerializer, GRNEntryWithPORefSerializer, GRNInvoiceSerializer, GoodsReceiptNoteSerializer, PPEntrySerializer, ProductSerializer, PurchaseInvoiceSerializer
from InvManage.scripts.filters import *
from InvManage.scripts.helpers import create_event
from InvManage.models.objects import GRNInvoice

from InvManage.scripts.helpers import generate_form_parameter_string
from django.http import HttpResponse, JsonResponse


def create_grn_view(request):
    """ 
        Creates a goods receipt note (GRN) on ``POST`` request, and returns a GRN creation form on ``GET`` request. 

        .. http:get:: /grn

            Gets the GRN creation form.

            **Example request**:

            .. sourcecode:: http

                GET /grn/ HTTP/1.1
                Host: localhost:8000
                Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
            
    
            **Example response**:

            .. sourcecode:: http

                HTTP/1.1 200 OK
                Vary: Accept
                Content-Type: text/html; charset=utf-8

            :reqheader Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
            :statuscode 200: GRN creation form received successfully.

        .. http:post:: /grn

            Creates a GRN.
            There are two modes:
            - ``auto`` : Setting ``grn-grnType`` to ``auto`` creates a GRN with PO reference.
            - ``manual`` : Setting ``grn-grnType`` to ``manual`` creates a GRN without PO reference. In this case
                            the ``grn-poRef`` is not required.

            **Example request**:

            .. sourcecode:: http

                POST /consumer/ HTTP/1.1
                Host: localhost:8000
                Content-Type: multipart/form-data;

            :form grn-grnType: ``auto``

            :form grn-vendor: ``4``

            :form grn-poRef: ``182``

            :form grn-amendNumber: ``546``

            :form grn-amendDate: ``2021-09-29``

            :form grn-identifier: ``846``

            :form grn-date: ``2021-09-29``

            :form grn-transporter: ``TeraTransport``

            :form grn-vehicleNumber: ``GH-646358``

            :form grn-gateInwardNumber: ``864353``

            :form grn-preparedBy: ``KJL``

            :form grn-checkedBy: ``KJH``

            :form grn-inspectedBy: ``GIO``

            :form grn-approvedBy: ``BHI``

            :form form-TOTAL_FORMS: ``3``

            :form form-INITIAL_FORMS: ``0``

            :form form-MIN_NUM_FORMS: ````

            :form form-MAX_NUM_FORMS: ````

            :form form-0-product: ``637``

            :form form-0-quantity: ``100``

            :form form-0-receivedQty: ``50``

            :form form-0-acceptedQty: ``50``

            :form form-0-rejectedQty: ``0``

            :form form-0-remark: ``OK``

            :form form-0-DELETE: ````

            :form form-0-grne_id: ``-1``

            :form form-0-ppe_id: ``324``

            :form form-1-product: ``645``

            :form form-1-quantity: ``250``

            :form form-1-receivedQty: ``200``

            :form form-1-acceptedQty: ``180``

            :form form-1-rejectedQty: ``20``

            :form form-1-remark: ``20 pieces faulty``

            :form form-1-DELETE: ````

            :form form-1-grne_id: ``-1``

            :form form-1-ppe_id: ``325``

            :form form-2-product: ``638``

            :form form-2-quantity: ``200``

            :form form-2-receivedQty: ``0``

            :form form-2-acceptedQty: ``0``

            :form form-2-rejectedQty: ``0``

            :form form-2-remark: ````

            :form form-2-DELETE: ````

            :form form-2-grne_id: ``-1``

            :form form-2-ppe_id: ``326``
                        
            :resheader Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryLTR88aZAnBUSE7mv
            :statuscode 302: Redirects to ``/grn``.

    """

    GRNEntryFormset = formset_factory(GRNEntryForm)
    data = {
        'form-TOTAL_FORMS': '0',
        'form-INITIAL_FORMS': '0',
        'form-MAX_NUM_FORMS': '',
    }
    grnentry_formset = GRNEntryFormset(data)
    grnentry_form = GRNEntryForm()
    if request.method == 'GET':
        grn_form = GRNInfo()
        prods = []
        for i, prod in enumerate(Product.objects.all()):
            prods.append({'id': prod.id, 'name': prod.name,
                          'code': prod.identifier})
        vendors = []
        for i, vend in enumerate(Vendor.objects.all()):
            vendors.append({'id': vend.id, 'name': vend.name})
        context = {
            'grn_form': grn_form,
            'grnentry_form': grnentry_form,
            'prods': prods,
            'vendors': vendors,
            'grnentry_formset': grnentry_formset,
            'grnes': {},
            'requested_view_type': 'create',
            'url': request.build_absolute_uri('/purchase_orders/')
        }
        return render(request, 'grn.html', context)
    
    if request.method == 'POST' and request.POST.get('grn-grnType') == 'manual': # For GRN WITHOUT poRef
        GRNEntryFormset = formset_factory(GRNEntryForm, can_delete=True)
        grn_form = GRNInfo(request.POST, prefix='grn')
        grnentry_formset = GRNEntryFormset(request.POST, prefix='form')
        data = {}
        print(grn_form.is_valid())
        print(grn_form.errors)
        print(grnentry_formset.is_valid())
        print(grnentry_formset.errors)
        grn_fields_without_poRef = ['date','vendor','identifier','grnType','amendNumber','amendDate','transporter','vehicleNumber','gateInwardNumber','preparedBy','checkedBy','inspectedBy','approvedBy']
        if grn_form.is_valid():
            for field in grn_fields_without_poRef:
                data[field]=grn_form.cleaned_data.get(field)            
            new_grn = GoodsReceiptNote.objects.create(**data)
            # Add Purchase Order references to the GRN
            grne_fields_without_poRef = ['grne_id','product','quantity','grn','remark','receivedQty','acceptedQty', 'rejectedQty']
            for grneform in grnentry_formset:
                validated_data={}
                for field in grne_fields_without_poRef:
                    validated_data[field]=grneform.cleaned_data.get(field)
                validated_data['product']=ProductSerializer(grneform.cleaned_data.get('product')).data
                validated_data['grn']=new_grn.pk
                grne_id = grneform.cleaned_data.get('grne_id')     
                if grne_id == -1:  # new grne to be created if id is -1
                    grnentry = GRNEntrySerializer(data=validated_data)
                    if grnentry.is_valid():
                        grnentry.save()
                        product = grneform.cleaned_data.get('product')
                        product.quantity += int(grneform.cleaned_data.get('acceptedQty'))  # Add the quantity to the product stock as it is new grn entry
                        product.save()
                    else:
                        print(grnentry.errors)
        create_event(new_grn,'Created')
        return redirect('grn')

    if request.method == 'POST' and request.POST.get('grn-grnType') == 'auto': # For GRN WITH poRef
        GRNEntryFormset = formset_factory(GRNEntryForm, can_delete=True)
        grn_form = GRNInfo(request.POST, prefix='grn')
        grnentry_formset = GRNEntryFormset(request.POST, prefix='form')
        data = {}
        # print(grn_form.is_valid())
        # print(grn_form.errors)
        # print(grnentry_formset.is_valid())
        # print(grnentry_formset.errors)
        grn_fields_with_poRef = ['date','vendor','identifier','grnType','amendNumber','amendDate','transporter','vehicleNumber','gateInwardNumber','preparedBy','checkedBy','inspectedBy','approvedBy']
        if grn_form.is_valid():
            for field in grn_fields_with_poRef:
                data[field]=grn_form.cleaned_data.get(field)
            print(data)
            new_grn = GoodsReceiptNote.objects.create(**data)
            # Add Purchase Order references to the GRN
            poRefs = grn_form.cleaned_data.get('poRef')
            for po in poRefs:
                new_grn.poRef.add(po)
            grne_fields_with_poRef = ['grne_id','product','quantity','grn','ppe_id','po_id','remark','receivedQty','acceptedQty', 'rejectedQty']
            for grneform in grnentry_formset:
                print(grneform.is_valid())
                validated_data={}
                if int(grneform.cleaned_data.get('receivedQty'))<=0: # for GRN type of PO reference, skip GRN entry creation if no quantity is received
                    continue
                for field in grne_fields_with_poRef:
                    validated_data[field]=grneform.cleaned_data.get(field)
                validated_data['po_id']=ProductPurchaseEntry.objects.get(id=grneform.cleaned_data.get('ppe_id')).order.pk
                validated_data['product']=ProductSerializer(grneform.cleaned_data.get('product')).data
                validated_data['grn']=new_grn.pk
                grne_id = grneform.cleaned_data.get('grne_id')     
                if grne_id == -1:  # new grne to be created if id is -1
                    grnentry = GRNEntryWithPORefSerializer(data=validated_data)
                    if grnentry.is_valid():
                        grnentry.save()
                        product = grneform.cleaned_data.get('product')
                        product.quantity += int(grneform.cleaned_data.get('acceptedQty'))  # Add the quantity to the product stock as it is new grn entry
                        product.save()
                    else:
                        print(grnentry.errors)
        create_event(new_grn,'Created')
        return redirect('grn')


def update_grn_view(request):
    """ 
        Updates the goods receipt note (GRN) on ``POST`` request, and returns a GRN update form on ``GET`` request. 

        .. http:get:: /grn/update

            Gets the GRN update form.

            **Example request**:

            .. sourcecode:: http

                GET /grn/update HTTP/1.1
                Host: localhost:8000
                Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
            
    
            **Example response**:

            .. sourcecode:: http

                HTTP/1.1 200 OK
                Vary: Accept
                Content-Type: text/html; charset=utf-8

            :reqheader Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
            :statuscode 200: GRN update form received successfully.

        .. http:post:: /grn/update

            Updates a GRN.
            There are two modes:
            - ``auto`` : Setting ``grn-grnType`` to ``auto`` creates a GRN with PO reference.
            - ``manual`` : Setting ``grn-grnType`` to ``manual`` creates a GRN without PO reference. In this case
                            the ``grn-poRef`` is not required.

            **Example request**:

            .. sourcecode:: http

                POST /consumer/ HTTP/1.1
                Host: localhost:8000
                Content-Type: multipart/form-data;

            :form grn-grnType: ``auto``

            :form grn-vendor: ``4``

            :form grn-poRef: ``182``

            :form grn-amendNumber: ``546``

            :form grn-amendDate: ``2021-09-29``

            :form grn-identifier: ``846``

            :form grn-date: ``2021-09-29``

            :form grn-transporter: ``TeraTransport``

            :form grn-vehicleNumber: ``GH-646358``

            :form grn-gateInwardNumber: ``864353``

            :form grn-preparedBy: ``KJL``

            :form grn-checkedBy: ``KJH``

            :form grn-inspectedBy: ``GIO``

            :form grn-approvedBy: ``BHI``

            :form form-TOTAL_FORMS: ``3``

            :form form-INITIAL_FORMS: ``0``

            :form form-MIN_NUM_FORMS: ````

            :form form-MAX_NUM_FORMS: ````

            :form form-0-product: ``637``

            :form form-0-quantity: ``100``

            :form form-0-receivedQty: ``50``

            :form form-0-acceptedQty: ``50``

            :form form-0-rejectedQty: ``0``

            :form form-0-remark: ``OK``

            :form form-0-DELETE: ````

            :form form-0-grne_id: ``-1``

            :form form-0-ppe_id: ``324``

            :form form-1-product: ``645``

            :form form-1-quantity: ``250``

            :form form-1-receivedQty: ``200``

            :form form-1-acceptedQty: ``180``

            :form form-1-rejectedQty: ``20``

            :form form-1-remark: ``20 pieces faulty``

            :form form-1-DELETE: ````

            :form form-1-grne_id: ``-1``

            :form form-1-ppe_id: ``325``

            :form form-2-product: ``638``

            :form form-2-quantity: ``200``

            :form form-2-receivedQty: ``0``

            :form form-2-acceptedQty: ``0``

            :form form-2-rejectedQty: ``0``

            :form form-2-remark: ````

            :form form-2-DELETE: ````

            :form form-2-grne_id: ``-1``

            :form form-2-ppe_id: ``326``
                        
            :resheader Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryLTR88aZAnBUSE7mv
            :statuscode 302: Redirects to ``/grn``.

    """

    if request.method == 'GET':
        ###### Fetch all the required data from the database ###########
        pk = request.GET.get('pk')
        print(pk)
        grn = GoodsReceiptNote.objects.get(id=pk)
        grnes = GoodsReceiptNote.objects.get(id=pk).grnentry_set.all()
        grn_data = grn.__dict__
        grn_data['vendor']=grn.vendor
        data = {
            'form-TOTAL_FORMS': len(grnes),
            'form-INITIAL_FORMS': len(grnes),
            'form-MAX_NUM_FORMS': '',
        }
        prods = []
        for i, prod in enumerate(Product.objects.all()):
            prods.append({'id': prod.id, 'name': prod.name,
                          'code': prod.identifier})
        vendors = []
        for i, vend in enumerate(Vendor.objects.all()):
            vendors.append({'id': vend.id, 'name': vend.name})
        grnes_serialized = []
        if grn.grnType == 'auto': # If the GRN has a po reference
            for grne in grnes:
                d = GRNEntryWithPORefSerializer(grne)
                grnes_serialized.append(d.data)
            grn_data['poRef'] = [po.pk for po in grn.poRef.all()]
        else: # If the GRN has no po references
            for grne in grnes:
                d = GRNEntrySerializer(grne)
                grnes_serialized.append(d.data)
        ######## Initialize forms for GRN and GRN Entries ##################
        GRNEntryFormset = formset_factory(GRNEntryForm, can_delete=True)
        grnentry_formset = GRNEntryFormset(data, initial=grnes)
        grnentry_form = GRNEntryForm()
        grn_form = GRNInfo(initial=grn_data)
        context = {
            'grn_form': grn_form,
            'grnentry_form': grnentry_form,
            'prods': prods,
            'vendors': vendors,
            'grnentry_formset': grnentry_formset,
            'grnes': grnes_serialized,
            'requested_view_type': 'update',
            'pk': pk,
        }
        return render(request, 'goods_receipt_note/update_grn.html', context)
    

    if request.method == 'POST':
        pk = request.POST.get('pk')
        grn = GoodsReceiptNote.objects.get(id=pk)
        if grn.grnType == 'manual':
            GRNEntryFormset = formset_factory(GRNEntryForm, can_delete=True)
            grn_form = GRNInfo(request.POST, prefix='grn')
            grnentry_formset = GRNEntryFormset(request.POST, prefix='form')
            data = {}
            print(grn_form.is_valid())
            print(grn_form.errors)
            print(grnentry_formset.is_valid())
            print(grnentry_formset.errors)
            grn_fields_without_poRef = ['date','vendor','identifier','grnType','amendNumber','amendDate','transporter','vehicleNumber','gateInwardNumber','preparedBy','checkedBy','inspectedBy','approvedBy']
            if grn_form.is_valid():
                for field in grn_fields_without_poRef:
                    data[field]=grn_form.cleaned_data.get(field)            
                GoodsReceiptNote.objects.filter(id=pk).update(**data)
                grne_fields_without_poRef = ['grne_id','product','quantity','grn','remark','receivedQty','acceptedQty', 'rejectedQty']
                for grneform in grnentry_formset:
                    if grneform.is_valid():
                        validated_data={}
                        if int(grneform.cleaned_data.get('receivedQty'))<=0: # for GRN type of PO reference, skip GRN entry creation if no quantity is received
                            continue
                        for field in grne_fields_without_poRef:
                            validated_data[field]=grneform.cleaned_data.get(field)
                        validated_data['product']=ProductSerializer(grneform.cleaned_data.get('product')).data
                        validated_data['grn']=pk
                        grne_id = grneform.cleaned_data.get('grne_id')
                        product = grneform.cleaned_data.get('product') 
                        if grne_id == -1:  # new ppe to be created if id is -1
                            grnentry = GRNEntrySerializer(data=validated_data)
                            if grnentry.is_valid():
                                grnentry.save()
                                product.quantity += int(grneform.cleaned_data.get('acceptedQty'))  # Add the quantity to the product stock as it is new ppe
                            else:
                                print(grnentry.errors)
                        else:
                            grne = GRNEntry.objects.get(id=grne_id)
                            old_accepted = grne.acceptedQty
                            old_received = grne.receivedQty
                            grnentry = GRNEntrySerializer(grne, data=validated_data)
                            if grnentry.is_valid():
                                grnentry.save()
                                product.quantity += int(grneform.cleaned_data.get('acceptedQty'))-old_accepted
                                product.save()  # Save the changes to the product instance
                            else:
                                print(grnentry.errors)
                for grneform in grnentry_formset.deleted_forms:
                    grne_id = grneform.cleaned_data.get('grne_id')
                    product = grneform.cleaned_data.get('product')
                    quantity = grneform.cleaned_data.get('acceptedQty')
                    if grne_id != -1:
                        ppe = GRNEntry.objects.get(id=grne_id)
                        product.quantity -= quantity
                        ppe.delete()
        if grn.grnType == 'auto':
            GRNEntryFormset = formset_factory(GRNEntryForm, can_delete=True)
            grn_form = GRNInfo(request.POST, prefix='grn')
            grnentry_formset = GRNEntryFormset(request.POST, prefix='form')
            data = {}
            grn_fields_with_poRef = ['date','identifier','amendNumber','amendDate','transporter','vehicleNumber','gateInwardNumber','preparedBy','checkedBy','inspectedBy','approvedBy']
            if grn_form.is_valid():
                for field in grn_fields_with_poRef:
                    data[field]=grn_form.cleaned_data.get(field)
                modified_grn = GoodsReceiptNote.objects.filter(id=pk).update(**data)
                grne_fields_with_poRef = ['grne_id','product','quantity','grn','ppe_id','po_id','remark','receivedQty','acceptedQty', 'rejectedQty']
                for grneform in grnentry_formset:
                    if grneform.is_valid():
                        validated_data={}
                        if int(grneform.cleaned_data.get('receivedQty'))<=0: # for GRN type of PO reference, skip GRN entry creation if no quantity is received
                            continue
                        for field in grne_fields_with_poRef:
                            validated_data[field]=grneform.cleaned_data.get(field)
                        validated_data['po_id']=ProductPurchaseEntry.objects.get(id=grneform.cleaned_data.get('ppe_id')).order.pk
                        validated_data['product']=ProductSerializer(grneform.cleaned_data.get('product')).data
                        validated_data['grn']=modified_grn
                        grne_id = grneform.cleaned_data.get('grne_id')
                        product = grneform.cleaned_data.get('product')    
                        if grne_id == -1:  # new ppe to be created if id is -1
                            grnentry = GRNEntryWithPORefSerializer(data=validated_data)
                            if grnentry.is_valid():
                                grnentry.save()
                                product.quantity += int(grneform.cleaned_data.get('acceptedQty'))  # Add the quantity to the product stock as it is new ppe
                            else:
                                print(grnentry.errors)
                        else:
                            grne = GRNEntry.objects.get(id=grne_id)
                            old_accepted = grne.acceptedQty
                            old_received = grne.receivedQty
                            grnentry = GRNEntryWithPORefSerializer(grne, data=validated_data)
                            if grnentry.is_valid():
                                grnentry.save()
                                product.quantity += int(grneform.cleaned_data.get('acceptedQty'))-old_accepted
                                product.save()  # Save the changes to the product instance
                            else:
                                print(grnentry.errors)
        create_event(GoodsReceiptNote.objects.get(id=pk),'Updated')
        # return redirect('grn')
        return HttpResponse(f'<p>{generate_form_parameter_string(request.POST)}</p>')


def delete_grn_view(request, pk):
    """ 
        Deletes the GRN with primary key ``object_id`` on ``POST`` request.

        .. http:post:: /grn/<str:object_id>/delete

            Deletes the GRN represented by the primary key ``object_id``.

            **Example request**:

            .. sourcecode:: http

                POST /grn/104/delete HTTP/1.1
                Host: localhost:8000
                Content-Type: application/x-www-form-urlencoded
                
            :param object_id: GRN primary key.
            :resheader Content-Type: application/x-www-form-urlencoded
            :statuscode 302: Redirects to ``/grn``.
            :statuscode 500: GRN matching query does not exist.

    """
    if request.method == 'POST':
        grn = GoodsReceiptNote.objects.get(id=pk)
        create_event(grn,'Deleted')
        grn.delete()
        return redirect('grn')
    


def display_grns_view(request):
    """ 
        Retrieves the list of GRNs on ``GET`` request.

        .. http:get:: /grns/

            Gets the list of all GRNs.

            **Example request**:

            .. sourcecode:: http

                GET /grns/ HTTP/1.1
                Host: localhost:8000
                Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
            
            :form page: The page number of the GRN list.
    
            **Example response**:

            .. sourcecode:: http

                HTTP/1.1 200 OK
                Vary: Accept
                Content-Type: text/html; charset=utf-8

            :reqheader Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
            :statuscode 200: List of GRNs received successfully.
    """
    if request.method == 'GET':
        grns = GoodsReceiptNote.objects.all()
        state = FilterState.objects.get(name='GRNs_basic')
        column_list = change_column_position(request, state)
        myFilter = GoodsReceiptNoteFilter(request.GET, queryset=grns)
        queryset = myFilter.qs
        number_of_objects = len(queryset)
        page_number = request.GET.get('page')
        page_obj, dictionaries = paginate(queryset, myFilter, page_number)
        # dictionary contains only vendor id and not vendor name. So add it.
        for dict in dictionaries:
            vend_id = dict['vendor_id']
            vendor = Vendor.objects.get(id=vend_id)
            dict['vendor'] = vendor.name
        return render(request, 'goods_receipt_note/grn_contents.html', {'page_obj': page_obj,
                                                                               'myFilter': myFilter,
                                                                               'n_prod': number_of_objects,
                                                                               'columns': column_list,
                                                                               'dicts': dictionaries,
                                                                               'url': request.build_absolute_uri('/grns/')})


def print_grn_view(request, pk):
    """ 
        Opens the GRN with primary key ``grn_id`` for printing on ``GET`` request.

        .. http:post:: /grn/<str:grn_id>/print

            Opens the GRN represented by the primary key ``grn_id``.

            **Example request**:

            .. sourcecode:: http

                POST /grn/103/print HTTP/1.1
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
                        "grn": {
                            "grnes": [
                                {
                                    "grn": 103,
                                    "grne_id": 117,
                                    "ppe_id": 324,
                                    "po_id": 293,
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
                                    "receivedQty": 50,
                                    "acceptedQty": 50,
                                    "rejectedQty": 0,
                                    "remark": "OK"
                                },
                                {
                                    "grn": 103,
                                    "grne_id": 118,
                                    "ppe_id": 325,
                                    "po_id": 293,
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
                                    "receivedQty": 200,
                                    "acceptedQty": 180,
                                    "rejectedQty": 20,
                                    "remark": "20 pieces faulty"
                                }
                            ],
                            "date": "29-Sep-2021",
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
                            "poRef": [
                                182
                            ],
                            "identifier": 846,
                            "grnType": "auto",
                            "amendDate": "2021-09-29T00:00:00Z",
                            "transporter": "TeraTransport",
                            "vehicleNumber": "GH-646358",
                            "gateInwardNumber": "864353",
                            "preparedBy": "KJL",
                            "checkedBy": "KJH",
                            "inspectedBy": "GIO",
                            "approvedBy": "BHI"
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
                
            :param grn_id: GRN primary key.
            :resheader Content-Type: application/json
            :statuscode 200: GRN print request successful.
            :statuscode 500: GRN matching query does not exist.

    """
    if request.method == 'GET':
        grn = GoodsReceiptNote.objects.get(id=pk)
        company = Company.objects.all().last()
        company_shippingaddress = company.shippingaddress
        vendor_communication = grn.vendor.communication
        invoice_serializer = GRNInvoiceSerializer(
            GRNInvoice(company=company, 
                            grn=grn, 
                            shippingaddress=company_shippingaddress, 
                            communication=vendor_communication))
        print(JsonResponse(invoice_serializer.data))
    return JsonResponse(invoice_serializer.data)
