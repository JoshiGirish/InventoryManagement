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


def create_grn_view(request):
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


def display_grns_view(request):
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


def delete_grn_view(request, pk):
    if request.method == 'POST':
        grn = GoodsReceiptNote.objects.get(id=pk)
        create_event(grn,'Deleted')
        grn.delete()
        return redirect('grn')


def update_grn_view(request):
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
        return redirect('grn')
    


def print_grn_view(request, pk):
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
