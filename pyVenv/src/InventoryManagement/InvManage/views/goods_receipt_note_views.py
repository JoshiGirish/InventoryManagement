from django.shortcuts import render
from django.shortcuts import redirect
from InvManage.forms import *
from django.forms.formsets import formset_factory
from InvManage.models import *
from InvManage.filters import GoodsReceiptNoteFilter
from django.http import JsonResponse
from InvManage.serializers import ProductSerializer, PPEntrySerializer, GRNEntrySerializer, GoodsReceiptNoteSerializer
from InvManage.scripts.filters import *
from InvManage.scripts.helpers import create_event


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
    if request.method == 'POST':
        print(request.POST)
        GRNEntryFormset = formset_factory(
            GRNEntryForm, can_delete=True)
        grn_form = GRNInfo(request.POST, prefix='grn')
        grnentry_formset = GRNEntryFormset(
            request.POST, prefix='form')
        data = {}
        print(grn_form.is_valid())
        print(grn_form.errors)
        print(grnentry_formset.is_valid())
        print(grnentry_formset.errors)
        grn_fields_without_poRef = ['date','vendor','identifier','grnType','amendDate','vehicleNumber','gateInwardNumber','preparedBy','checkedBy','inspectedBy','approvedBy']
        grn_fields_with_poRef = ['date','poRef','identifier','grnType','amendDate','vehicleNumber','gateInwardNumber','preparedBy','checkedBy','inspectedBy','approvedBy']
        if grn_form.is_valid():
            if request.POST.get('grn-grnType') == 'manual':
                for field in grn_fields_without_poRef:
                    data[field]=grn_form.cleaned_data.get(field)
            elif request.POST.get('grn-grnType') == 'auto':
                for field in grn_fields_with_poRef:
                    data[field]=grn_form.cleaned_data.get(field)
            
            new_grn = GoodsReceiptNote.objects.create(**data)
            grne_fields_without_poRef = ['grne_id','product','quantity','grn','remark','receivedQty','acceptedQty', 'rejectedQty']
            grne_fields_with_poRef = ['grne_id','product','quantity','grn','ppes','remark','receivedQty','acceptedQty', 'rejectedQty']
            for grneform in grnentry_formset:
                validated_data={}
                if request.POST.get('grn-grnType') == 'manual':
                    for field in grne_fields_without_poRef:
                        validated_data[field]=grneform.cleaned_data.get(field)
                    validated_data['ppes']=None
                elif request.POST.get('grn-grnType') == 'auto':
                    if grneform.cleaned_data.get('receivedQty')<=0: # for GRN type of PO reference, skip GRN entry creation if no quantity is received
                        continue
                    for field in grne_fields_with_poRef:
                        validated_data[field]=grneform.cleaned_data.get(field)
                    validated_data['ppes']=PPEntrySerializer(grneform.cleaned_data.get('ppes')).data
                validated_data['product']=ProductSerializer(grneform.cleaned_data.get('product')).data
                validated_data['grn']=new_grn.pk
                grne_id = grneform.cleaned_data.get('grne_id')     
                if grne_id == -1:  # new grne to be created if id is -1
                    grnentry = GRNEntrySerializer(data=validated_data)
                    if grnentry.is_valid():
                        grnentry.save()
                        product = grneform.cleaned_data.get('product')
                        product.quantity += grneform.cleaned_data.get('quantity')  # Add the quantity to the product stock as it is new grn entry
                    else:
                        print(grnentry.errors)
        create_event(new_grn,'Created')
        return redirect('grn')


def display_grns_view(request):
    if request.method == 'GET':
        grns = GoodsReceiptNote.objects.all()
        state = FilterState.objects.get(name='POs_basic')
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
        return render(request, 'purchase_order/purchase_order_contents.html', {'page_obj': page_obj,
                                                                               'myFilter': myFilter,
                                                                               'n_prod': number_of_objects,
                                                                               'columns': column_list,
                                                                               'dicts': dictionaries,
                                                                               'url': request.build_absolute_uri('/purchase_orders/')})


def delete_grn_view(request, pk):
    if request.method == 'POST':
        grn = GoodsReceiptNote.objects.get(id=pk)
        create_event(grn,'Deleted')
        grn.delete()
        return redirect('purchase_order')


def update_grn_view(request):
    if request.method == 'GET':
        pk = request.GET.get('pk')
        print(pk)
        grn = GoodsReceiptNote.objects.get(id=pk)
        grn_data = grn.__dict__
        vendor = grn.vendor
        ven_data = vendor.__dict__
        company = Company.objects.all().last()
        ship_data = company.shippingaddress.__dict__
        GRNEntryFormset = formset_factory(
            GRNEntryForm, can_delete=True)
        grnes = GoodsReceiptNote.objects.get(id=pk).productpurchaseentry_set.all()
        grnes_serialized = []
        for ppe in grnes:
            d = PPEntrySerializer(ppe)
            grnes_serialized.append(d.data)
        data = {
            'form-TOTAL_FORMS': len(grnes),
            'form-INITIAL_FORMS': len(grnes),
            'form-MAX_NUM_FORMS': '',
        }
        print(grnes_serialized)
        grnentry_formset = GRNEntryFormset(data, initial=grnes)
        grnentry_form = GRNEntryForm()
        grn_form = GRNInfo(initial=grn_data)
        # print(grn_form)
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
            'grn_form': grn_form,
            'grnentry_form': grnentry_form,
            'prods': prods,
            'vendor_id': vendor.pk,
            'vendors': vendors,
            'vendor_form': vendor_form,
            'grnentry_formset': grnentry_formset,
            'grnes': grnes_serialized,
            'shipping_form': shipping_form,
            'requested_view_type': 'update',
            'pk': pk,
        }
        return render(request, 'purchase_order/update_purchase_order.html', context)
    if request.method == 'POST':
        pk = request.POST.get('pk')
        print(pk)
        GRNEntryFormset = formset_factory(
            GRNEntryForm, can_delete=True)
        grn_form = GRNInfo(request.POST, prefix='grn')
        grnentry_formset = GRNEntryFormset(
            request.POST, prefix='form')
        data = {}
        print(grn_form.is_valid())
        print(grnentry_formset.is_valid())
        if grn_form.is_valid():
            vendor = grn_form.cleaned_data.get('vendor')
            grn = grn_form.cleaned_data.get('grn')
            date = grn_form.cleaned_data.get('date')
            tax = grn_form.cleaned_data.get('tax')
            discount = grn_form.cleaned_data.get('discount')
            paid = grn_form.cleaned_data.get('paid')
            balance = grn_form.cleaned_data.get('balance')
            subtotal = grn_form.cleaned_data.get('subtotal')
            taxtotal = grn_form.cleaned_data.get('taxtotal')
            ordertotal = grn_form.cleaned_data.get('ordertotal')
            data = {
                'vendor': vendor,
                'grn': grn,
                'date': date,
                'tax': tax,
                'discount': discount,
                'paid': paid,
                'balance': balance,
                'subtotal': subtotal,
                'taxtotal': taxtotal,
                'ordertotal': ordertotal
            }
            GoodsReceiptNote.objects.filter(id=pk).update(**data)
            for grneform in grnentry_formset:
                if grneform.is_valid():
                    grne_id = grneform.cleaned_data.get('grne_id')
                    product = grneform.cleaned_data.get('product')
                    quantity = grneform.cleaned_data.get('quantity')
                    price = grneform.cleaned_data.get('price')
                    discount = grneform.cleaned_data.get('discount')
                    order = GoodsReceiptNote.objects.get(id=pk)
                    print(grne_id)
                    validated_data = {'grne_id': grne_id,
                                    #   'product': product.__dict__,
                                      'product': ProductSerializer(product).data,
                                      'quantity': quantity,
                                      'price': price,
                                      'discount': discount,
                                      'order': pk,
                                      }
                    if grne_id == -1:  # new ppe to be created if id is -1
                        pentry = PPEntrySerializer(data=validated_data)
                        if pentry.is_valid():
                            pentry.save()
                            product.quantity += quantity  # Add the quantity to the product stock as it is new ppe
                        else:
                            print(pentry.errors)
                    else:
                        ppe = GRNEntry.objects.get(id=grne_id)
                        # print(ppe)
                        old_quantity = ppe.quantity
                        # grneform.cleaned_data.update({'order':order})
                        # validated_data.update({'grne_id': grne_id})
                        # print(validated_data)
                        pentry = PPEntrySerializer(ppe, data=validated_data)
                        if pentry.is_valid():
                            # print(validated_data)
                            pentry.save()
                            # GRNEntry.objects.filter(id=grne_id).update(product=product,quantity=quantity,price=price,discount=discount,order=order)
                            # Add the difference of quantity to the product stock as it is updated ppe
                            product.quantity += quantity-old_quantity
                            product.save()  # Save the changes to the product instance
                        else:
                            print(pentry.errors)
            for grneform in grnentry_formset.deleted_forms:
                print(grneform.is_valid())
                grne_id = grneform.cleaned_data.get('grne_id')
                print(grne_id)
                product = grneform.cleaned_data.get('product')
                quantity = grneform.cleaned_data.get('quantity')
                if grne_id != -1:
                    ppe = GRNEntry.objects.get(id=grne_id)
                    product.quantity -= quantity
                    ppe.delete()
        create_event(GoodsReceiptNote.objects.get(id=pk),'Updated')
        return redirect('purchase_order')


def print_grn_view(request, pk):
    if request.method == 'GET':
        grn = GoodsReceiptNote.objects.get(id=pk)
        company = Company.objects.all().last()
        company_shippingaddress = company.shippingaddress
        vendor_communication = grn.vendor.communication
        # print(shippingaddress)
        invoice_serializer = PurchaseInvoiceSerializer(
            PurchaseInvoice(company=company, 
                            grn=grn, 
                            shippingaddress=company_shippingaddress, 
                            communication=vendor_communication))
        print(JsonResponse(invoice_serializer.data))
    return JsonResponse(invoice_serializer.data)
