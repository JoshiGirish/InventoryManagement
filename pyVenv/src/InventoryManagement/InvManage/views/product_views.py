from django.shortcuts import render
from django.shortcuts import redirect
from InvManage.forms import *
from InvManage.models import *
from django.core.files.storage import FileSystemStorage
import io,csv
from InvManage.filters import ProductFilter
from InvManage.scripts.filters import *
from InvManage.scripts.helpers import create_event
from InvManage.scripts.helpers import create_event
from InvManage.scripts.helpers import generate_form_parameter_string
from django.http import HttpResponse, JsonResponse



def create_product_view(request):
    """ 
        Creates a product on ``POST`` request, and returns a product creation form on ``GET`` request. 

        .. http:get:: /product

            Gets the product creation form.

            **Example request**:

            .. sourcecode:: http

                GET /product/ HTTP/1.1
                Host: localhost:8000
                Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
            
    
            **Example response**:

            .. sourcecode:: http

                HTTP/1.1 200 OK
                Vary: Accept
                Content-Type: text/html; charset=utf-8

            :reqheader Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
            :statuscode 200: Product creation form received successfully.

        .. http:post:: /product

            Creates a product.

            **Example request**:

            .. sourcecode:: http

                POST /product/ HTTP/1.1
                Host: localhost:8000
                Content-Type: multipart/form-data;
                
            :form basic-name: ``Yamaha FS100C Acoustic Guitar``

            :form basic-item_type: ``Black Acoustic Guitar``

            :form basic-category: ``Musical Instrument``

            :form basic-description: ``Top: Spruce back/sides, Mahogany neck, Nato fret board, Rosewood bridge, Snorkeling frets: 20, Open chrome tuners, Finishes: Black``

            :form detailed-length: ``1056``

            :form detailed-width: ``376``

            :form detailed-height: ``140``

            :form detailed-weight: ``3.2``

            :form storage-barcode: ``036000029145``

            :form storage-expiry: ``2040-09-29``

            :form status-quantity: ``20``

            :form status-identifier: ``FS100C``

            :form status-location: ``BAY004``

            :form pricing-price: ``9990``

            :form pricing-discount: ``7``
            
            :resheader Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryLTR88aZAnBUSE7mv
            :statuscode 302: Redirects to ``/product``.

    """
    if request.method == 'GET':
        basic_form = ProductBasicInfoForm()
        detailed_form = ProductDetailedInfoForm()
        thumbnail_form = ThumbnailForm()
        storage_form = ProductStorageInfoForm()
        pricing_form = ProductPricingForm()
        status_form = ProductStatusForm()	
        return render(request, 'product.html',{'basic_form':basic_form,
                                                    'thumbnail_form':thumbnail_form,
                                                    'detailed_form':detailed_form,
                                                    'storage_form':storage_form,
                                                    'pricing_form':pricing_form,
                                                    'status_form':status_form,
                                                    'requested_view_type':'create'})
    if request.method == 'POST':
        types = [ProductBasicInfoForm, ProductDetailedInfoForm, ThumbnailForm, ProductStorageInfoForm, ProductPricingForm, ProductStatusForm]
        # types = [basic_form, detailed_form, thumnail_form, storage_form, pricing_form]
        data = {}
        print(request.POST)
        for form_type in types:
            pre = form_type.prefix
            form = form_type(request.POST, prefix = pre)
            if form.is_valid():
                data.update(form.cleaned_data)
        uploaded_file = request.FILES['thumbnail-image']
        data.update({'image':uploaded_file})
        fs = FileSystemStorage()
        fs.save(uploaded_file.name,uploaded_file)
        new_prod = Product.objects.create(**data)
        create_event(new_prod,'Created')
        return redirect('product')

def update_product_view(request):
    """ 
        Updates a product on ``POST`` request and returns the product update form on ``GET`` request. 

        .. http:get:: /product/update

            Gets the product update form whose primary key matches the query parameter ``pk``.

            **Example request**:

            .. sourcecode:: http

                GET /product/update HTTP/1.1
                Host: localhost:8000
                Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
            
            :query pk: The primary key of the product.
            
            **Example response**:

            .. sourcecode:: http

                HTTP/1.1 200 OK
                Vary: Accept
                Content-Type: text/html; charset=utf-8

            :reqheader Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
            :statuscode 200: Product update form received successfully.

        .. http:post:: /product/update

            Updates the product.

            **Example request**:

            .. sourcecode:: http

                POST /product/update HTTP/1.1
                Host: localhost:8000
                Content-Type: multipart/form-data;
                
            :form pk: ``778``
    
            :form basic-name: ``Yamaha FS100C Acoustic Guitar``

            :form basic-item_type: ``Black Acoustic Guitar``

            :form basic-category: ``Musical Instrument``

            :form basic-description: ``Top: Spruce back/sides, Mahogany neck, Nato fret board, Rosewood bridge, Snorkeling frets: 20, Open chrome tuners, Finishes: Black``

            :form detailed-length: ``1056``

            :form detailed-width: ``376``

            :form detailed-height: ``140``

            :form detailed-weight: ``3.2``

            :form storage-barcode: ``036000029145``

            :form storage-expiry: ``2040-09-29``

            :form status-quantity: ``20``

            :form status-identifier: ``FS100C``

            :form status-location: ``BAY004``

            :form pricing-price: ``9990``

            :form pricing-discount: ``7``

            :resheader Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryLTR88aZAnBUSE7mv
            :statuscode 302: Redirects to ``/product``.

    """
    if request.method == 'GET':
        pk = request.GET.get('pk')
        product = Product.objects.get(id=pk)
        data = product.__dict__
        basic_form = ProductBasicInfoForm(initial=data)
        detailed_form = ProductDetailedInfoForm(initial=data)
        thumnail_form = ThumbnailForm(initial=data)
        storage_form = ProductStorageInfoForm(initial=data)
        pricing_form = ProductPricingForm(initial=data)
        status_form = ProductStatusForm(initial=data)
        thumbnail = product.image.name
        return render(request, 'product.html',{'basic_form':basic_form,
                                            'thumbnail_form':thumnail_form,
                                            'detailed_form':detailed_form,
                                            'storage_form':storage_form,
                                            'pricing_form':pricing_form,
                                            'status_form':status_form,
                                            'thumbnail':thumbnail,
                                            'requested_view_type':'update',
                                            'pk':pk})
    if request.method == 'POST':
        pk = request.POST.get('pk')
        types = [ProductBasicInfoForm, ProductDetailedInfoForm, ThumbnailForm, ProductStorageInfoForm, ProductPricingForm, ProductStatusForm]
        data = {}
        for form_type in types:
            pre = form_type.prefix
            form = form_type(request.POST, prefix = pre)
            if form.is_valid():
                data.update(form.cleaned_data)
        uploaded_file = request.FILES['thumbnail-image']
        data.update({'image':uploaded_file})
        print('Printing DATA:',data)
        Product.objects.filter(id=pk).update(**data)
        fs = FileSystemStorage()
        fs.save(uploaded_file.name,uploaded_file)
        create_event(Product.objects.get(id=pk),'Updated')
        return redirect('/product')


def delete_product_view(request,pk):
    """ 
        Deletes the product with primary key ``product_id`` on ``POST`` request.

        .. http:post:: /product/<str:product_id>/delete

            Deletes the consumer represented by the primary key ``product_id``.

            **Example request**:

            .. sourcecode:: http

                POST /product/778/delete HTTP/1.1
                Host: localhost:8000
                Content-Type: application/x-www-form-urlencoded
                
            :param product_id: Product primary key.
            :resheader Content-Type: application/x-www-form-urlencoded
            :statuscode 302: Redirects to ``/product``.
            :statuscode 500: Prodcut matching query does not exist.

    """
    if request.method == 'POST':
        prod_id = pk
        # prod_id = request.POST.get('product_id')
        prod = Product.objects.get(id=prod_id)
        create_event(prod,'Deleted')
        prod.delete()
        return redirect('/product')
    

def display_products_view(request):
    """ 
        Retrieves the list of products on ``GET`` request.

        .. http:get:: /products/

            Gets the list of all products.

            **Example request**:

            .. sourcecode:: http

                GET /products/ HTTP/1.1
                Host: localhost:8000
                Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
            
            :form page: The page number of the products list.
    
            **Example response**:

            .. sourcecode:: http

                HTTP/1.1 200 OK
                Vary: Accept
                Content-Type: text/html; charset=utf-8

            :reqheader Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
            :statuscode 200: List of products received successfully.
    """
    if request.method == 'GET':
        products = Product.objects.all()
        state = FilterState.objects.get(name='Products_basic')
        column_list = change_column_position(request, state)
        myFilter = ProductFilter(request.GET, queryset=products)
        queryset = myFilter.qs
        number_of_products = len(queryset)
        page_number = request.GET.get('page')
        page_obj, dictionaries = paginate(queryset,myFilter,page_number)
        return render(request, 'display/product_contents.html',{'page_obj':page_obj,
                                                        'myFilter':myFilter,
                                                        'n_prod': number_of_products,
                                                        'columns': column_list,
                                                        'dicts': dictionaries,
                                                        'url': request.build_absolute_uri('/products/')})
        

def uploadCSV(request,data):
    """ 
        Imports products into database from a ``.csv`` file on ``POST`` request.
        CSV template columns: ``name``, ``category``, ``item_type``, ``description``, ``price``, ``quantity``, ``identifier``, ``location``, ``length``, ``width``, ``height``, ``weight``, ``discount``, ``barcode``, ``expiry``.

        .. http:post:: /upload/<data>/

            Imports product data.

            **Example request**:

            .. sourcecode:: http

                POST /product/778/delete HTTP/1.1
                Host: localhost:8000
                
            :statuscode 302: Redirects to ``/product``.

    """
    return_url = 'product'
    if request.method == "POST":
        print("\n\n ---------------------------------- POST ----------------------------------")
        print(request)
        print(request.POST)
        # Decides which fucntion needs to be called to handle the upload
        def upload_router(data):
            route = {
                'products': (create_products,'/product'),
                'vendors': (create_vendors,'/vendor')
            }
            return route.get(data)
        # Function which creates products from the uploaded file
        def create_products(io_string):
            for column in csv.reader(io_string, delimiter=',', quotechar="|"):
                _, created = Product.objects.update_or_create(
                    name=column[0],
                    category=column[1],
                    item_type=column[2],
                    description=column[3],
                    price=column[4],
                    quantity=column[5],
                    identifier=column[6],
                    location=column[7],
                    length=column[8],
                    width=column[9],
                    height=column[10],
                    weight=column[11],
                    discount=column[12],
                    barcode=column[13],
                    expiry=column[14],
                )
            return
        # Function which creates vendors from the uploaded file
        def create_vendors(io_string):
            for column in csv.reader(io_string, delimiter='|'):
                _, created = Vendor.objects.update_or_create(
                    name=column[0],
                    identifier=column[1],
                    phone=column[2],
                    address=column[3],
                    email=column[4],
                    location=column[5],
                )
            return
        csv_file = request.FILES.get('file')
        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)
        route_func,return_url = upload_router(data)  # Get the function and return url
        route_func(io_string) # Execute the route function
        return redirect(return_url)
