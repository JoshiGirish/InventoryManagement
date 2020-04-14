from django.shortcuts import render
from django.shortcuts import redirect
from .forms import *
from django.forms.formsets import formset_factory
from .models import Product, Vendor, PurchaseOrder, ProductPurchaseEntry, Company, Invoice, ShippingAddress
from django.core.files.storage import FileSystemStorage
import io,csv
from .filters import ProductFilter, VendorFilter, PurchaseOrderFilter, CompanyFilter
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.db import IntegrityError, transaction
from .serializers import VendorSerializer, PPEntrySerializer, PurchaseOrderSerializer, InvoiceSerializer

def create_company_view(request):
	if request.method == 'GET':
		company_form = CompanyForm()
		thumbnail_form = ThumbnailForm()
		shipping_form = ShippingAddressForm()
		return render(request, 'company/company.html', {'company_form': company_form,
												'thumbnail_form': thumbnail_form,
												'shipping_form': shipping_form})
	if request.method == 'POST':
		comp_data = {}
		ship_data = {}
		company_form = CompanyForm(request.POST,prefix=CompanyForm.prefix)
		thumbnail_form = ThumbnailForm(request.POST,prefix=ThumbnailForm.prefix)
		shipping_form = ShippingAddressForm(request.POST, prefix= ShippingAddressForm.prefix)
		if company_form.is_valid() and shipping_form.is_valid():
			comp_data.update(company_form.cleaned_data)
			ship_data.update(shipping_form.cleaned_data)
		shippigaddress = ShippingAddress.objects.create(**ship_data)
		comp_data.update({'shippingaddress': shippigaddress})
		uploaded_file = request.FILES['thumbnail-image']
		comp_data.update({'image':uploaded_file})
		Company.objects.create(**comp_data)
		return redirect('/company')

def update_company_view(request,pk):
	if request.method == 'GET':
		company = Company.objects.get(id=pk)
		data = company.__dict__
		company_form = CompanyForm(initial=data)
		ship = company.shippingaddress.__dict__
		shipping_form = ShippingAddressForm(initial=ship)
		thumbnail = company.image.name
		return render(request, 'company/update_company.html', {'company_form': company_form,
												'thumbnail': thumbnail,
												'shipping_form': shipping_form})
	if request.method == 'POST':
		comp_data = {}
		ship_data = {}
		company_form = CompanyForm(request.POST,prefix=CompanyForm.prefix)
		thumbnail_form = ThumbnailForm(request.POST,prefix=ThumbnailForm.prefix)
		shipping_form = ShippingAddressForm(request.POST, prefix= ShippingAddressForm.prefix)
		print(company_form.is_valid())
		print(shipping_form.is_valid())
		if company_form.is_valid():
			comp_data.update(company_form.cleaned_data)
			ship_data.update(shipping_form.cleaned_data)
		shippigaddress = ShippingAddress.objects.create(**ship_data)
		comp_data.update({'shippingaddress': shippigaddress})
		uploaded_file = request.FILES['thumbnail-image']
		comp_data.update({'image':uploaded_file})
		Company.objects.filter(id=pk).update(**comp_data)
		fs = FileSystemStorage()
		fs.save(uploaded_file.name,uploaded_file)
		return redirect('/companies')

def delete_company_view(request,pk):
	if request.method == 'POST':
		company = Company.objects.get(id=pk)
		company.delete()
		return redirect('/companies')

def display_companies_view(request):
	if request.method == 'GET':
		companies = Company.objects.all()
		myFilter = CompanyFilter(request.GET, queryset=companies)
		products = myFilter.qs
		number_of_companies = len(companies)
		paginator = Paginator(companies,15)
		page_number = request.GET.get('page')
		page_obj = paginator.get_page(page_number)
		return render(request, 'company/companies.html',{'page_obj':page_obj,'myFilter':myFilter, 'n_prod': number_of_companies})

def create_product_view(request):
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
													'status_form':status_form})
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
		Product.objects.create(**data)
		fs = FileSystemStorage()
		fs.save(uploaded_file.name,uploaded_file)
		return redirect('/products')

def delete_product_view(request,pk):
	if request.method == 'POST':
		prod_id = pk
		# prod_id = request.POST.get('product_id')
		prod = Product.objects.get(id=prod_id)
		prod.delete()
		return redirect('/products')

def display_products_view(request):
	if request.method == 'GET':
		products = Product.objects.all()
		myFilter = ProductFilter(request.GET, queryset=products)
		products = myFilter.qs
		number_of_products = len(products)
		paginator = Paginator(products,15)
		page_number = request.GET.get('page')
		page_obj = paginator.get_page(page_number)
		return render(request, 'display/products.html',{'page_obj':page_obj,'myFilter':myFilter, 'n_prod': number_of_products})

def update_product_view(request,pk):
	if request.method == 'GET':
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
											'thumbnail':thumbnail})
	if request.method == 'POST':
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
		return redirect('/products')

def uploadCSV(request,data):
	return_url = '/products'
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
	data = {
		'form-TOTAL_FORMS': '0',
	    'form-INITIAL_FORMS': '0',
		'form-MAX_NUM_FORMS': '',
		}
	pentry_formset = ProductPurchaseEntryFormset(data)
	pentry_form = ProductPurchaseEntryForm()
	shipping_form = ShippingAddressForm()
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
			'pentry_formset': pentry_formset,
			'ppes': {},
			'shipping_form': shipping_form,
		}	
		return render(request, 'purchase_order.html',context)
	if request.method == 'POST':
		purchase_form = PurchaseOrderBasicInfo(request.POST, prefix='po')
		pentry_formset = ProductPurchaseEntryFormset(request.POST,prefix = 'form')
		data = {}
		if purchase_form.is_valid() and pentry_formset.is_valid():
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
			for ppeform in pentry_formset:
				product = ppeform.cleaned_data.get('product')
				quantity = ppeform.cleaned_data.get('quantity')
				price = ppeform.cleaned_data.get('price')
				discount = ppeform.cleaned_data.get('discount')
				order = new_po
				ProductPurchaseEntry.objects.create(product=product,quantity=quantity,price=price,discount=discount,order=order)
				product.quantity += quantity # Add the purchased quantity to the product stock
				product.save() # Save the changes to the product instance
		return redirect('/purchase_orders')

def display_purchase_orders_view(request):
	if request.method == 'GET':
		pos = PurchaseOrder.objects.all()
		myFilter = PurchaseOrderFilter(request.GET, queryset=pos)
		pos = myFilter.qs
		number_of_vendors = len(pos)
		paginator = Paginator(pos,15)
		page_number = request.GET.get('page')
		page_obj = paginator.get_page(page_number)
		return render(request, 'purchase_order/purchase_orders.html',{'page_obj':page_obj,'myFilter':myFilter, 'n_prod': number_of_vendors})

def delete_purchase_order_view(request,pk):
	if request.method == 'POST':
		po = PurchaseOrder.objects.get(id=pk)
		po.delete()
		return redirect('/purchase_orders')

def update_purchase_order_view(request,pk):
	po = PurchaseOrder.objects.get(id=pk)
	po_data = po.__dict__
	vendor = po.vendor
	ven_data = vendor.__dict__
	if request.method == 'GET':
		ProductPurchaseEntryFormset = formset_factory(ProductPurchaseEntryForm)
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
		pentry_formset = ProductPurchaseEntryFormset(data,initial=ppes)
		pentry_form = ProductPurchaseEntryForm()
		purchase_form = PurchaseOrderBasicInfo(initial=po_data)
		print(purchase_form)
		vendor_form = VendorForm(initial=ven_data)
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
			'vendor_id': vendor.pk,
			'vendors': vendors,
			'vendor_form': vendor_form,
			'pentry_formset': pentry_formset,
			'ppes': ppes_serialized,
		}	
		return render(request, 'purchase_order/update_purchase_order.html',context)
	if request.method == 'POST':
		purchase_form = PurchaseOrderBasicInfo(request.POST, prefix='po')
		pentry_formset = ProductPurchaseEntryFormset(request.POST,prefix = 'form')
		data = {}
		if purchase_form.is_valid() and pentry_formset.is_valid():
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
			for ppeform in pentry_formset:
				product = ppeform.cleaned_data.get('product')
				quantity = ppeform.cleaned_data.get('quantity')
				price = ppeform.cleaned_data.get('price')
				discount = ppeform.cleaned_data.get('discount')
				order = new_po
				ProductPurchaseEntry.objects.create(product=product,quantity=quantity,price=price,discount=discount,order=order)
				product.quantity += quantity # Add the purchased quantity to the product stock
				product.save() # Save the changes to the product instance
		return redirect('/products')

def print_purchase_order_view(request,pk):
	if request.method == 'GET':
		po = PurchaseOrder.objects.get(id=pk)
		company = Company.objects.all().last()
		shippingaddress = company.shippingaddress
		print(shippingaddress)
		invoice_serializer = InvoiceSerializer(Invoice(company=company,po=po,shippingaddress=shippingaddress))
	return JsonResponse(invoice_serializer.data)

def create_vendor_view(request):
	if request.method == 'GET':
		vendors = []
		for i,vend in enumerate(Vendor.objects.all()):
			vendors.append({'id':vend.id,'name':vend.name,'code':vend.identifier})
		vendor_form = VendorForm()	
		return render(request, 'vendor/create_vendor.html',{'vendor_form': vendor_form, 'vendors': vendors})
	if request.method == 'POST':
		data = {}
		form = VendorForm(request.POST, prefix = 'vend')
		if form.is_valid():
			data.update(form.cleaned_data)
		Vendor.objects.create(**data)
		return redirect('/vendors')

def delete_vendor_view(request, pk):
	if request.method == 'POST':
		vendor = Vendor.objects.get(id=pk)
		vendor.delete()
		return redirect('/vendors')

def get_vendor(request):
	if request.method == 'GET':
		vendor_id = request.GET.get('vendor_id')
		vendor = VendorSerializer(Vendor.objects.get(id=vendor_id))
		return JsonResponse(vendor.data)

def display_vendors_view(request):
	if request.method == 'GET':
		vendors = Vendor.objects.all()
		myFilter = VendorFilter(request.GET, queryset=vendors)
		vendors = myFilter.qs
		number_of_vendors = len(vendors)
		paginator = Paginator(vendors,15)
		page_number = request.GET.get('page')
		page_obj = paginator.get_page(page_number)
		return render(request, 'vendor/vendors.html',{'page_obj':page_obj,'myFilter':myFilter, 'n_prod': number_of_vendors})
	
def update_vendor_view(request,pk):
	if request.method == 'GET':
		vendor = Vendor.objects.get(id=pk)
		data = vendor.__dict__
		vendor_form = VendorForm(initial=data)
		return render(request, 'vendor/update_vendor.html',{'vendor_form': vendor_form})
	if request.method == 'POST':
		data = {}
		form = VendorForm(request.POST, prefix = 'vend')
		if form.is_valid():
			data.update(form.cleaned_data)
		print('Printing DATA:',data)
		Vendor.objects.filter(id=pk).update(**data)
		return redirect('/vendors')



	