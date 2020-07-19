from django.shortcuts import render
from django.shortcuts import redirect
from InvManage.forms import *
from django.forms.formsets import formset_factory
from InvManage.models import *
from InvManage.filters import SalesOrderFilter
from django.http import JsonResponse
from InvManage.serializers import ProductSerializer, PSEntrySerializer, SalesInvoiceSerializer
from InvManage.scripts.filters import *


def create_sales_order_view(request):
    ProductSalesEntryFormset = formset_factory(ProductSalesEntryForm)
    data = {
        'form-TOTAL_FORMS': '0',
        'form-INITIAL_FORMS': '0',
        'form-MAX_NUM_FORMS': '',
    }
    pentry_formset = ProductSalesEntryFormset(data)
    pentry_form = ProductSalesEntryForm()
    shipping_form = ShippingAddressForm()
    company = Company.objects.all().last()
    ship_data = company.shippingaddress.__dict__
    if request.method == 'GET':
        shipping_form = ShippingAddressForm(initial=ship_data)
        sales_form = SalesOrderBasicInfo()
        consumer_form = ConsumerForm()
        prods = []
        for i, prod in enumerate(Product.objects.all()):
            prods.append({'id': prod.id, 'name': prod.name,
                          'code': prod.identifier})
        consumers = []
        for i, consumer in enumerate(Consumer.objects.all()):
            consumers.append({'id': consumer.id, 'name': consumer.name})
        context = {
            'sales_form': sales_form,
            'pentry_form': pentry_form,
            'prods': prods,
            'consumers': consumers,
            'consumer_form': consumer_form,
            'pentry_formset': pentry_formset,
            'pses': {},
            'shipping_form': shipping_form,
            'requested_view_type': 'create',
        }
        return render(request, 'sales_order.html', context)
    if request.method == 'POST':
        ProductSalesEntryFormset = formset_factory(
            ProductSalesEntryForm, can_delete=True)
        sales_form = SalesOrderBasicInfo(request.POST, prefix='so')
        pentry_formset = ProductSalesEntryFormset(
            request.POST, prefix='form')
        data = {}
        print(sales_form.is_valid())
        print(sales_form.errors)
        print(pentry_formset.is_valid())
        print(pentry_formset.errors)
        if sales_form.is_valid():
            consumer = sales_form.cleaned_data.get('consumer')
            so = sales_form.cleaned_data.get('so')
            date = sales_form.cleaned_data.get('date')
            tax = sales_form.cleaned_data.get('tax')
            discount = sales_form.cleaned_data.get('discount')
            paid = sales_form.cleaned_data.get('paid')
            balance = sales_form.cleaned_data.get('balance')
            subtotal = sales_form.cleaned_data.get('subtotal')
            taxtotal = sales_form.cleaned_data.get('taxtotal')
            ordertotal = sales_form.cleaned_data.get('ordertotal')
            data = {
                'consumer': consumer,
                'so': so,
                'date': date,
                'tax': tax,
                'discount': discount,
                'paid': paid,
                'balance': balance,
                'subtotal': subtotal,
                'taxtotal': taxtotal,
                'ordertotal': ordertotal
            }
            new_so = SalesOrder.objects.create(**data)
            for pseform in pentry_formset:
                if pseform.is_valid():
                    pse_id = pseform.cleaned_data.get('pse_id')
                    product = pseform.cleaned_data.get('product')
                    quantity = pseform.cleaned_data.get('quantity')
                    price = pseform.cleaned_data.get('price')
                    discount = pseform.cleaned_data.get('discount')
                    order = SalesOrder.objects.get(id=new_so.pk)
                    print(pse_id)
                    validated_data = {'pse_id': pse_id,
                                      'product': ProductSerializer(product).data,
                                      'quantity': quantity,
                                      'price': price,
                                      'discount': discount,
                                      'order': new_so.pk,
                                      }
                    if pse_id == -1:  # new pse to be created if id is -1
                        pentry = PSEntrySerializer(data=validated_data)
                        print(pentry.is_valid())
                        if pentry.is_valid():
                            pentry.save()
                            product.quantity -= quantity  # Subtract the quantity to the product stock as it is new pse
                            product.save()
                        else:
                            print(pentry.errors)
        return redirect('sales_order')


def display_sales_orders_view(request):
    if request.method == 'GET':
        sos = sort_ascending_descending(request, SalesOrder)
        state = FilterState.objects.get(name='SOs_basic')
        column_list = change_column_position(request, state)
        myFilter = SalesOrderFilter(request.GET, queryset=sos)
        queryset = myFilter.qs
        number_of_objects = len(queryset)
        page_number = request.GET.get('page')
        page_obj, dictionaries = paginate(queryset, myFilter, page_number)
        # dictionary contains only consumer id and not consumer name. So add it.
        for dict in dictionaries:
            consumer_id = dict['consumer_id']
            consumer = Consumer.objects.get(id=consumer_id)
            dict['consumer'] = consumer.name
        return render(request, 'sales_order/sales_order_contents.html', {'page_obj': page_obj,
                                                                               'myFilter': myFilter,
                                                                               'n_prod': number_of_objects,
                                                                               'columns': column_list,
                                                                               'dicts': dictionaries})


def delete_sales_order_view(request, pk):
    if request.method == 'POST':
        so = SalesOrder.objects.get(id=pk)
        so.delete()
        return redirect('sales_order')


def update_sales_order_view(request):
    if request.method == 'GET':
        pk = request.GET.get('pk')
        print(pk)
        so = SalesOrder.objects.get(id=pk)
        so_data = so.__dict__
        consumer = so.consumer
        ven_data = consumer.__dict__
        company = Company.objects.all().last()
        ship_data = company.shippingaddress.__dict__
        ProductSalesEntryFormset = formset_factory(
            ProductSalesEntryForm, can_delete=True)
        pses = SalesOrder.objects.get(id=pk).productsalesentry_set.all()
        pses_serialized = []
        for pse in pses:
            d = PSEntrySerializer(pse)
            pses_serialized.append(d.data)
        data = {
            'form-TOTAL_FORMS': len(pses),
            'form-INITIAL_FORMS': len(pses),
            'form-MAX_NUM_FORMS': '',
        }
        print(pses_serialized)
        pentry_formset = ProductSalesEntryFormset(data, initial=pses)
        pentry_form = ProductSalesEntryForm()
        sales_form = SalesOrderBasicInfo(initial=so_data)
        # print(sales_form)
        consumer_form = ConsumerForm(initial=ven_data)
        shipping_form = ShippingAddressForm(initial=ship_data)
        prods = []
        for i, prod in enumerate(Product.objects.all()):
            prods.append({'id': prod.id, 'name': prod.name,
                          'code': prod.identifier})
        consumers = []
        for i, consumer in enumerate(Consumer.objects.all()):
            consumers.append({'id': consumer.id, 'name': consumer.name})
        context = {
            'sales_form': sales_form,
            'pentry_form': pentry_form,
            'prods': prods,
            'consumer_id': consumer.pk,
            'consumers': consumers,
            'consumer_form': consumer_form,
            'pentry_formset': pentry_formset,
            'pses': pses_serialized,
            'shipping_form': shipping_form,
            'requested_view_type': 'update',
            'pk': pk,
        }
        return render(request, 'sales_order/update_sales_order.html', context)
    if request.method == 'POST':
        pk = request.POST.get('pk')
        print(pk)
        ProductSalesEntryFormset = formset_factory(
            ProductSalesEntryForm, can_delete=True)
        sales_form = SalesOrderBasicInfo(request.POST, prefix='so')
        pentry_formset = ProductSalesEntryFormset(
            request.POST, prefix='form')
        data = {}
        print(sales_form.is_valid())
        print(pentry_formset.is_valid())
        if sales_form.is_valid():
            consumer = sales_form.cleaned_data.get('consumer')
            so = sales_form.cleaned_data.get('so')
            date = sales_form.cleaned_data.get('date')
            tax = sales_form.cleaned_data.get('tax')
            discount = sales_form.cleaned_data.get('discount')
            paid = sales_form.cleaned_data.get('paid')
            balance = sales_form.cleaned_data.get('balance')
            subtotal = sales_form.cleaned_data.get('subtotal')
            taxtotal = sales_form.cleaned_data.get('taxtotal')
            ordertotal = sales_form.cleaned_data.get('ordertotal')
            data = {
                'consumer': consumer,
                'so': so,
                'date': date,
                'tax': tax,
                'discount': discount,
                'paid': paid,
                'balance': balance,
                'subtotal': subtotal,
                'taxtotal': taxtotal,
                'ordertotal': ordertotal
            }
            SalesOrder.objects.filter(id=pk).update(**data)
            for pseform in pentry_formset:
                if pseform.is_valid():
                    pse_id = pseform.cleaned_data.get('pse_id')
                    product = pseform.cleaned_data.get('product')
                    quantity = pseform.cleaned_data.get('quantity')
                    price = pseform.cleaned_data.get('price')
                    discount = pseform.cleaned_data.get('discount')
                    order = SalesOrder.objects.get(id=pk)
                    print(pse_id)
                    validated_data = {'pse_id': pse_id,
                                    #   'product': product.__dict__,
                                      'product': ProductSerializer(product).data,
                                      'quantity': quantity,
                                      'price': price,
                                      'discount': discount,
                                      'order': pk,
                                      }
                    if pse_id == -1:  # new pse to be created if id is -1
                        pentry = PSEntrySerializer(data=validated_data)
                        print(pentry.is_valid())
                        if pentry.is_valid():
                            pentry.save()
                            product.quantity -= quantity  # Subtract the quantity to the product stock as it is new pse
                            print(f'Decreasing stock of the {product.name} product by {quantity}.')
                        else:
                            print(pentry.errors)
                    else:
                        pse = ProductSalesEntry.objects.get(id=pse_id)
                        # print(pse)
                        old_quantity = pse.quantity
                        # pseform.cleaned_data.update({'order':order})
                        # validated_data.update({'pse_id': pse_id})
                        # print(validated_data)
                        pentry = PSEntrySerializer(pse, data=validated_data)
                        if pentry.is_valid():
                            # print(validated_data)
                            pentry.save()
                            # ProductSalesEntry.objects.filter(id=pse_id).update(product=product,quantity=quantity,price=price,discount=discount,order=order)
                            # Subtract the difference of quantity to the product stock as it is updated pse
                            product.quantity -= quantity-old_quantity
                            product.save()  # Save the changes to the product instance
                        else:
                            print(pentry.errors)
            for pseform in pentry_formset.deleted_forms:
                print(pseform.is_valid())
                pse_id = pseform.cleaned_data.get('pse_id')
                print(pse_id)
                product = pseform.cleaned_data.get('product')
                quantity = pseform.cleaned_data.get('quantity')
                if pse_id != -1:
                    pse = ProductSalesEntry.objects.get(id=pse_id)
                    product.quantity -= quantity
                    pse.delete()
        return redirect('sales_order')


def print_sales_order_view(request, pk):
    if request.method == 'GET':
        so = SalesOrder.objects.get(id=pk)
        company = Company.objects.all().last()
        shippingaddress = company.shippingaddress
        print(shippingaddress)
        invoice_serializer = SalesInvoiceSerializer(
            SalesInvoice(company=company, so=so, shippingaddress=shippingaddress))
        print(invoice_serializer.data)
    return JsonResponse(invoice_serializer.data)
