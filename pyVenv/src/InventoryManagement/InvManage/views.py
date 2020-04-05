from django.shortcuts import render
from django.shortcuts import redirect
from .forms import *
from .models import Product, Vendor, PurchaseOrder
from django.core.files.storage import FileSystemStorage
import io,csv
from .filters import ProductFilter
from django.core.paginator import Paginator
from django.http import HttpResponse

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

def uploadCSV(request):
	if request.method == "POST":
		csv_file = request.FILES.get('file')
	data_set = csv_file.read().decode('UTF-8')
	io_string = io.StringIO(data_set)
	next(io_string)
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
			barcode=column[13]
		)
	return redirect('/products')
		
def create_purchase_order_view(request):
	if request.method == 'GET':
		prods = []
		for i,prod in enumerate(Product.objects.all()):
			prods.append({'id':prod.id,'name':prod.name,'code':prod.identifier})
		purchase_form = PurchaseOrderBasicInfo()	
		return render(request, 'purchase_order.html',{'purchase_form': purchase_form, 'prods': prods})
	if request.method == 'POST':
		print(request.POST)
		types = ['PurchaseOrderBasicInfo']
		# types = [basic_form, detailed_form, thumnail_form, storage_form, pricing_form]
		data = {}
		print(request.POST)
		for form_type in types:
			pre = form_type.prefix
			form = form_type(request.POST, prefix = pre)
			if form.is_valid():
				data.update(form.cleaned_data)
		PurchaseOrder.objects.create(**data)
		fs = FileSystemStorage()
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
