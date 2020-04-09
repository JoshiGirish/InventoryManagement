from django.shortcuts import render
from django.shortcuts import redirect
from .forms import *
from django.forms.formsets import formset_factory
from .models import Product, Vendor, PurchaseOrder, ProductPurchaseEntry
from django.core.files.storage import FileSystemStorage
import io,csv
from .filters import ProductFilter
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.db import IntegrityError, transaction
from .serializers import VendorSerializer

def create_product_view(request):
	if request.method == 'GET':
		basic_form = ProductBasicInfoForm()
		detailed_form = ProductDetailedInfoForm()
		thumbnail_form = ProductThumbnailForm()
		storage_form = ProductStorageInfoForm()
		pricing_form = ProductPricingForm()
		status_form = ProductStatusForm()	
		return render(request, 'product.html',{'basic_form':basic_form,
													'thumbnail_form':thumbnail_form,
													'detailed_form':detailed_form,
													'storage_form':storage_form,
													'pricing_form':pricing_form,
													'status_form':status_form})
	if request.method == 'POST':
		types = [ProductBasicInfoForm, ProductDetailedInfoForm, ProductThumbnailForm, ProductStorageInfoForm, ProductPricingForm, ProductStatusForm]
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
		Product.objects.create(**data)
		fs = FileSystemStorage()
		fs.save(uploaded_file.name,uploaded_file)
		return redirect('/products')

def products_view(request):
	products = Product.objects.all()
	myFilter = ProductFilter(request.GET, queryset=products)
	products = myFilter.qs
	number_of_products = len(products)
	paginator = Paginator(products,10)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	return render(request, 'display/products.html',{'page_obj':page_obj,'myFilter':myFilter, 'n_prod': number_of_products})

def update_product_view(request,pk):
	product = Product.objects.get(id=pk)
	data = product.__dict__
	basic_form = ProductBasicInfoForm(initial=data)
	detailed_form = ProductDetailedInfoForm(initial=data)
	thumnail_form = ProductThumbnailForm(initial=data)
	storage_form = ProductStorageInfoForm(initial=data)
	pricing_form = ProductPricingForm(initial=data)
	status_form = ProductStatusForm(initial=data)
	thumbnail = product.image.name
	if request.method == 'POST':
		types = [ProductBasicInfoForm, ProductDetailedInfoForm, ProductThumbnailForm, ProductStorageInfoForm, ProductPricingForm, ProductStatusForm]
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
		return redirect('/products')

	return render(request, 'product.html',{'basic_form':basic_form,
											'thumbnail_form':thumnail_form,
											'detailed_form':detailed_form,
											'storage_form':storage_form,
											'pricing_form':pricing_form,
											'status_form':status_form,
											'thumbnail':thumbnail})

def delete_product_view(request):
	prod_id = request.POST.get('product_id')
	prod = Product.objects.get(id=prod_id)
	prod.delete()
	return redirect('/products')

def uploadCSV(request,data):
	return_url = '/products'
	if request.method == 'GET':
		pass

	if request.method == "POST":
		# Decides which fucntion needs to be called to handle the upload
		def upload_router(data):
			route = {
				'products': (create_products,'/products'),
				'vendors': (create_vendors,'/products')
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


def create_purchase_order_view(request):
	ProductPurchaseEntryFormset = formset_factory(ProductPurchaseEntryForm)
	pentry_formset = ProductPurchaseEntryFormset()
	pentry_form = ProductPurchaseEntryForm()
	print(pentry_form)

	if request.method == 'GET':
		purchase_form = PurchaseOrderBasicInfo()
		vendor_form = VendorForm()
		prods = []
		for i,prod in enumerate(Product.objects.all()):
			prods.append({'id':prod.id,'name':prod.name,'code':prod.identifier})
		vendors = []
		for i,vend in enumerate(Vendor.objects.all()):
			vendors.append({'id': vend.id,'name':vend.name})
		context = {
			'purchase_form': purchase_form,
			'pentry_form': pentry_form,
			'prods': prods,
			'vendors': vendors,
			'vendor_form': vendor_form,
			'pentry_formset': pentry_formset
		}	
		return render(request, 'purchase_order.html',context)

	if request.method == 'POST':
		# print(request.POST)
		purchase_form = PurchaseOrderBasicInfo(request.POST, prefix='po')
		print(purchase_form)
		pentry_formset = ProductPurchaseEntryFormset(request.POST,prefix = 'form')
		data = {}
		print(purchase_form.is_valid())
		print(pentry_formset.is_valid())
		if purchase_form.is_valid() and pentry_formset.is_valid():
			vendor = purchase_form.cleaned_data.get('vendor')
			# vendor = Vendor.objects.get(id=vendor_id)
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
				'vendor':vendor,
				'po':po,
				'date':date,
				'tax':tax,
				'discount':discount,
				'paid':paid,
				'balance':balance,
				'subtotal':subtotal,
				'taxtotal':taxtotal,
				'ordertotal':ordertotal
			}
			new_po = PurchaseOrder.objects.create(**data)
			# PurchaseOrder.objects.create(**data)

            # # create purchase entries
			# purchase_entries = []
			for ppeform in pentry_formset:
				product = ppeform.cleaned_data.get('product')
				quantity = ppeform.cleaned_data.get('quantity')
				price = ppeform.cleaned_data.get('price')
				discount = ppeform.cleaned_data.get('discount')
				order = new_po
				ProductPurchaseEntry.objects.create(product=product,quantity=quantity,price=price,discount=discount,order=order)

		return redirect('/products')	

def create_vendor_view(request):
	if request.method == 'GET':
		vendors = []
		for i,vend in enumerate(Vendor.objects.all()):
			vendors.append({'id':vend.id,'name':vend.name,'code':vend.identifier})
		vendor_form = VendorForm()	
		return render(request, 'vendor.html',{'vendor_form': vendor_form, 'vendors': vendors})

	if request.method == 'POST':
		data = {}
		form = VendorForm(request.POST, prefix = VendorForm.prefix)
		if form.is_valid():
			data.update(form.cleaned_data)
		Vendor.objects.create(**data)
		return redirect('/products')

def get_vendor(request):
	print(request.GET)
	vendor_id = request.GET.get('vendor_id')
	vendor = VendorSerializer(Vendor.objects.get(id=vendor_id))
	return JsonResponse(vendor.data)

	