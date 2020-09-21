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


def create_purchase_order_view(request):
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
                            product.quantity += quantity  # Add the quantity to the product stock as it is new ppe
                        else:
                            print(pentry.errors)
        create_event(new_po,'Created')
        return redirect('purchase_order')


def display_purchase_orders_view(request):
    if request.method == 'GET':
        pos = PurchaseOrder.objects.all()
        state = FilterState.objects.get(name='POs_basic')
        column_list = change_column_position(request, state)
        myFilter = PurchaseOrderFilter(request.GET, queryset=pos)
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


def delete_purchase_order_view(request, pk):
    if request.method == 'POST':
        po = PurchaseOrder.objects.get(id=pk)
        create_event(po,'Deleted')
        po.delete()
        return redirect('purchase_order')


def update_purchase_order_view(request):
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
                        # print(ppe)
                        old_quantity = ppe.quantity
                        # ppeform.cleaned_data.update({'order':order})
                        # validated_data.update({'ppe_id': ppe_id})
                        # print(validated_data)
                        pentry = PPEntrySerializer(ppe, data=validated_data)
                        if pentry.is_valid():
                            # print(validated_data)
                            pentry.save()
                            # ProductPurchaseEntry.objects.filter(id=ppe_id).update(product=product,quantity=quantity,price=price,discount=discount,order=order)
                            # Add the difference of quantity to the product stock as it is updated ppe
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
        return redirect('purchase_order')


def print_purchase_order_view(request, pk):
    if request.method == 'GET':
        po = PurchaseOrder.objects.get(id=pk)
        company = Company.objects.all().last()
        company_shippingaddress = company.shippingaddress
        vendor_communication = po.vendor.communication
        # print(shippingaddress)
        invoice_serializer = PurchaseInvoiceSerializer(
            PurchaseInvoice(company=company, 
                            po=po, 
                            shippingaddress=company_shippingaddress, 
                            communication=vendor_communication))
        print(JsonResponse(invoice_serializer.data))
    return JsonResponse(invoice_serializer.data)
