from django.shortcuts import render
from django.shortcuts import redirect
from InvManage.forms import *
from django.forms.formsets import formset_factory
from InvManage.models import *
from InvManage.filters import SalesOrderFilter
from django.http import JsonResponse
from InvManage.serializers import ProductSerializer, PSEntrySerializer, SalesInvoiceSerializer
from InvManage.scripts.filters import *
from InvManage.scripts.helpers import create_event
from InvManage.scripts.helpers import generate_form_parameter_string
from django.http import HttpResponse, JsonResponse


def create_sales_order_view(request):
    """ 
        Creates a sales order (SO) on ``POST`` request, and returns a SO creation form on ``GET`` request. 

        .. http:get:: /sales_order

            Gets the sales order creation form.

            **Example request**:

            .. sourcecode:: http

                GET /sales_order/ HTTP/1.1
                Host: localhost:8000
                Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
            
    
            **Example response**:

            .. sourcecode:: http

                HTTP/1.1 200 OK
                Vary: Accept
                Content-Type: text/html; charset=utf-8

            :reqheader Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
            :statuscode 200: Sales order creation form received successfully.

        .. http:post:: /sales_order

            Creates a sales order.

            **Example request**:

            .. sourcecode:: http

                POST /sales_order/ HTTP/1.1
                Host: localhost:8000
                Content-Type: multipart/form-data;

            :form so-consumer: ``5``

            :form consumer-name: ``The Music Store``

            :form consumer-identifier: ``CONS1256``

            :form consumer-gstin: ``89ACC654654335``

            :form consumer-phone: ``+91 8325642358``

            :form consumer-address: ``Plot no 958, N- 4, Neo Complex, Barh, Wokha, Nagaland, 797111``

            :form consumer-email: ``JohnDoe@themusic.store``

            :form consumer-location: ``Wokha``

            :form so-so: ``465``

            :form so-date: ``2021-09-30``

            :form so-tax: ``12``

            :form so-discount: ``8``

            :form so-paid: ``4500``

            :form so-balance: ``1200``

            :form ship-title: ``FingDocks``

            :form ship-name: ``Harding Gross``

            :form ship-phone: ``936 651-4847``

            :form ship-address: ``8798 At, St., 7639``

            :form ship-city: ``Rome``

            :form ship-state: ``Lazio``

            :form ship-country: ``Italy``

            :form ship-website: ``http://fringdocs.com``

            :form ship-post: ``300326``

            :form so-subtotal: ``94600.00``

            :form so-taxtotal: ``7568.00``

            :form so-ordertotal: ``102168.00``

            :form form-TOTAL_FORMS: ``2``

            :form form-INITIAL_FORMS: ``0``

            :form form-MIN_NUM_FORMS: ````

            :form form-MAX_NUM_FORMS: ````

            :form form-0-product: ``645``

            :form form-0-quantity: ``450``

            :form form-0-price: ``120``

            :form form-0-discount: ``10``

            :form form-0-DELETE: ````

            :form form-0-pse_id: ``-1``

            :form form-1-product: ``654``

            :form form-1-quantity: ``500``

            :form form-1-price: ``100``

            :form form-1-discount: ``8``

            :form form-1-DELETE: ````

            :form form-1-pse_id: ``-1``
                        
            :resheader Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryLTR88aZAnBUSE7mv
            :statuscode 302: Redirects to ``/sales_order``.

    """

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
                        # print(pentry.is_valid())
                        if pentry.is_valid():
                            pentry.save()
                            product.quantity -= quantity  # Subtract the quantity to the product stock as it is new pse
                            product.save()
                        else:
                            print(pentry.errors)
        create_event(new_so,'Created')
        return redirect('sales_order')



def update_sales_order_view(request):
    """ 
        Updates a sales order on ``POST`` request and returns the sales order update form for ``GET`` request. 

        .. http:get:: /sales_order/update

            Gets the sales order update form whose primary key matches the query parameter ``pk``.

            **Example request**:

            .. sourcecode:: http

                GET /sales_order/update HTTP/1.1
                Host: localhost:8000
                Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
            
            :query pk: The primary key of the sales order.
            
            **Example response**:

            .. sourcecode:: http

                HTTP/1.1 200 OK
                Vary: Accept
                Content-Type: text/html; charset=utf-8

            :reqheader Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
            :statuscode 200: Sales order update form received successfully.

        .. http:post:: /sales_order/update

            Updates the sales order.

            **Example request**:

            .. sourcecode:: http

                POST /sales_order/update HTTP/1.1
                Host: localhost:8000
                Content-Type: multipart/form-data;
    
            :form pk: ``30``

            :form so-consumer: ``7``

            :form consumer-name: ``The Music Store``

            :form consumer-identifier: ``CONS1256``

            :form consumer-gstin: ``89AAC4633353643``

            :form consumer-phone: ``+91 8325642358``

            :form consumer-address: ``Plot no 958, N- 4, Neo Complex, Barh, Wokha, Nagaland, 797111``

            :form consumer-email: ``JohnDoe@themusic.store``

            :form consumer-location: ``Wokha``

            :form so-so: ``465``

            :form so-date: ``2021-09-30``

            :form so-tax: ``10``

            :form so-discount: ``8.0``

            :form so-paid: ``4500.0``

            :form so-balance: ``1200.0``

            :form ship-title: ``FingDocks``

            :form ship-name: ``Harding Gross``

            :form ship-phone: ``936 651-4847``

            :form ship-address: ``8798 At, St., 7639``

            :form ship-city: ``Rome``

            :form ship-state: ``Lazio``

            :form ship-country: ``Italy``

            :form ship-website: ``http://fringdocs.com``

            :form ship-post: ``300326``

            :form so-subtotal: ``94600.0``

            :form so-taxtotal: ``7568.0``

            :form so-ordertotal: ``102168.0``

            :form form-TOTAL_FORMS: ``2``

            :form form-INITIAL_FORMS: ``2``

            :form form-MIN_NUM_FORMS: ````

            :form form-MAX_NUM_FORMS: ````

            :form form-0-product: ``645``

            :form form-0-quantity: ``450``

            :form form-0-price: ``120``

            :form form-0-discount: ``10``

            :form form-0-DELETE: ````

            :form form-0-pse_id: ``67``

            :form form-1-product: ``654``

            :form form-1-quantity: ``500``

            :form form-1-price: ``100``

            :form form-1-discount: ``8``

            :form form-1-DELETE: ````

            :form form-1-pse_id: ``68``

            :resheader Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryLTR88aZAnBUSE7mv
            :statuscode 302: Redirects to ``/sales_order``.

    """
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
        create_event(SalesOrder.objects.get(id=pk),'Updated')
        return redirect('sales_order')


def delete_sales_order_view(request, pk):
    """ 
        Deletes the sales order with primary key ``object_id`` on ``POST`` request.

        .. http:post:: /sales_order/<str:object_id>/delete

            Deletes the sales order represented by the primary key ``object_id``.

            **Example request**:

            .. sourcecode:: http

                POST /sales_order/30/delete HTTP/1.1
                Host: localhost:8000
                Content-Type: application/x-www-form-urlencoded
                
            :param object_id: Sales order primary key.
            :resheader Content-Type: application/x-www-form-urlencoded
            :statuscode 302: Redirects to ``/sales_order``.
            :statuscode 500: Sales order matching query does not exist.

    """
    if request.method == 'POST':
        so = SalesOrder.objects.get(id=pk)
        create_event(so,'Deleted')
        so.delete()
        return redirect('sales_order')


def display_sales_orders_view(request):
    """ 
        Retrieves the list of sales orders on ``GET`` request.

        .. http:get:: /sales_orders/

            Gets the list of all sales orders.

            **Example request**:

            .. sourcecode:: http

                GET /sales_orders/ HTTP/1.1
                Host: localhost:8000
                Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
            
            :form page: The page number of the sales order list.
    
            **Example response**:

            .. sourcecode:: http

                HTTP/1.1 200 OK
                Vary: Accept
                Content-Type: text/html; charset=utf-8

            :reqheader Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
            :statuscode 200: List of sales orders received successfully.
    """
    if request.method == 'GET':
        sos = SalesOrder.objects.all()
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
                                                                               'dicts': dictionaries,
                                                                               'url': request.build_absolute_uri('/sales_orders/')})

def print_sales_order_view(request, pk):
    """ 
        Opens the sales order with primary key ``so_id`` for printing on ``GET`` request.

        .. http:post:: /purchase_order/<str:so_id>/print

            Opens the sales order represented by the primary key ``so_id``.

            **Example request**:

            .. sourcecode:: http

                POST /sales_order/182/print HTTP/1.1
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
                        "so": {
                            "consumer": {
                                "name": "The Music Store",
                                "identifier": "CONS1256",
                                "gstin": "89AAC4633353643",
                                "phone": "+91 8325642358",
                                "address": "Plot no 958, N- 4, Neo Complex, Barh, Wokha, Nagaland, 797111",
                                "email": "JohnDoe@themusic.store",
                                "location": "Wokha"
                            },
                            "date": "2021-09-25T00:00:00Z",
                            "so": 89,
                            "subtotal": 744900.0,
                            "taxtotal": 59592.0,
                            "ordertotal": 804492.0,
                            "pses": [
                                {
                                    "pse_id": 64,
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
                                    "quantity": 50,
                                    "price": 9900.0,
                                    "discount": 10.0,
                                    "order": 29
                                },
                                {
                                    "pse_id": 65,
                                    "product": {
                                        "pk": 649,
                                        "name": "Sabar",
                                        "category": "Amet Consulting",
                                        "quantity": 3903,
                                        "identifier": "PROD21",
                                        "location": "Serang",
                                        "description": "High Sierra Sabar, Travel bag, Blue, Grey, Zipper, 36.5 L, 51.5 cm, 26 cm ",
                                        "prod_id": 649
                                    },
                                    "quantity": 25,
                                    "price": 4800.0,
                                    "discount": 8.0,
                                    "order": 29
                                },
                                {
                                    "pse_id": 66,
                                    "product": {
                                        "pk": 654,
                                        "name": "Parai",
                                        "category": "Aliquet Lobortis Ltd",
                                        "quantity": 8534,
                                        "identifier": "PROD26",
                                        "location": "Burhaniye",
                                        "description": "Kannan musical instruments Parai 15\" inch (Baffallow skin) Daf Instrument",
                                        "prod_id": 654
                                    },
                                    "quantity": 35,
                                    "price": 6000.0,
                                    "discount": 10.0,
                                    "order": 29
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
                        }
                    }
                ]            
                
            :param so_id: Sales order primary key.
            :resheader Content-Type: application/json
            :statuscode 200: Sales order print request successful.
            :statuscode 500: Sales order matching query does not exist.

    """
    if request.method == 'GET':
        so = SalesOrder.objects.get(id=pk)
        company = Company.objects.all().last()
        shippingaddress = company.shippingaddress
        print(shippingaddress)
        invoice_serializer = SalesInvoiceSerializer(
            SalesInvoice(company=company, so=so, shippingaddress=shippingaddress))
        print(invoice_serializer.data)
    return JsonResponse(invoice_serializer.data)
