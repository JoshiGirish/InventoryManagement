from django.shortcuts import render
from django.shortcuts import redirect
from InvManage.forms import *
from django.forms.formsets import formset_factory
from InvManage.models import *
from InvManage.filters import PurchaseOrderFilter
from django.http import JsonResponse
from InvManage.serializers import ProductSerializer, PPEntrySerializer, PurchaseInvoiceSerializer
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
        vendor_form = VendorForm()
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
            'vendor_form': vendor_form,
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
        grn_form = PurchaseOrderBasicInfo(request.POST, prefix='grn')
        grnentry_formset = GRNEntryFormset(
            request.POST, prefix='form')
        data = {}
        print(grn_form.is_valid())
        print(grnentry_formset.is_valid())
        print(grnentry_formset.errors)
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
            new_grn = PurchaseOrder.objects.create(**data)
            for ppeform in grnentry_formset:
                if ppeform.is_valid():
                    ppe_id = ppeform.cleaned_data.get('ppe_id')
                    product = ppeform.cleaned_data.get('product')
                    quantity = ppeform.cleaned_data.get('quantity')
                    price = ppeform.cleaned_data.get('price')
                    discount = ppeform.cleaned_data.get('discount')
                    order = PurchaseOrder.objects.get(id=new_grn.pk)
                    print(ppe_id)
                    validated_data = {'ppe_id': ppe_id,
                                      'product': ProductSerializer(product).data,
                                      'quantity': quantity,
                                      'price': price,
                                      'discount': discount,
                                      'order': new_grn.pk,
                                      }
                    if ppe_id == -1:  # new ppe to be created if id is -1
                        pentry = PPEntrySerializer(data=validated_data)
                        if pentry.is_valid():
                            pentry.save()
                            product.quantity += quantity  # Add the quantity to the product stock as it is new ppe
                        else:
                            print(pentry.errors)
        create_event(new_grn,'Created')
        return redirect('purchase_order')


def display_grns_view(request):
    if request.method == 'GET':
        grns = PurchaseOrder.objects.all()
        state = FilterState.objects.get(name='POs_basic')
        column_list = change_column_position(request, state)
        myFilter = PurchaseOrderFilter(request.GET, queryset=grns)
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
        grn = PurchaseOrder.objects.get(id=pk)
        create_event(grn,'Deleted')
        grn.delete()
        return redirect('purchase_order')


def update_grn_view(request):
    if request.method == 'GET':
        pk = request.GET.get('pk')
        print(pk)
        grn = PurchaseOrder.objects.get(id=pk)
        grn_data = grn.__dict__
        vendor = grn.vendor
        ven_data = vendor.__dict__
        company = Company.objects.all().last()
        ship_data = company.shippingaddress.__dict__
        GRNEntryFormset = formset_factory(
            GRNEntryForm, can_delete=True)
        grnes = PurchaseOrder.objects.get(id=pk).productpurchaseentry_set.all()
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
        grn_form = PurchaseOrderBasicInfo(initial=grn_data)
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
        grn_form = PurchaseOrderBasicInfo(request.POST, prefix='grn')
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
            PurchaseOrder.objects.filter(id=pk).update(**data)
            for ppeform in grnentry_formset:
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
                        ppe = GRNEntry.objects.get(id=ppe_id)
                        # print(ppe)
                        old_quantity = ppe.quantity
                        # ppeform.cleaned_data.update({'order':order})
                        # validated_data.update({'ppe_id': ppe_id})
                        # print(validated_data)
                        pentry = PPEntrySerializer(ppe, data=validated_data)
                        if pentry.is_valid():
                            # print(validated_data)
                            pentry.save()
                            # GRNEntry.objects.filter(id=ppe_id).update(product=product,quantity=quantity,price=price,discount=discount,order=order)
                            # Add the difference of quantity to the product stock as it is updated ppe
                            product.quantity += quantity-old_quantity
                            product.save()  # Save the changes to the product instance
                        else:
                            print(pentry.errors)
            for ppeform in grnentry_formset.deleted_forms:
                print(ppeform.is_valid())
                ppe_id = ppeform.cleaned_data.get('ppe_id')
                print(ppe_id)
                product = ppeform.cleaned_data.get('product')
                quantity = ppeform.cleaned_data.get('quantity')
                if ppe_id != -1:
                    ppe = GRNEntry.objects.get(id=ppe_id)
                    product.quantity -= quantity
                    ppe.delete()
        create_event(PurchaseOrder.objects.get(id=pk),'Updated')
        return redirect('purchase_order')


def print_grn_view(request, pk):
    if request.method == 'GET':
        grn = PurchaseOrder.objects.get(id=pk)
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
