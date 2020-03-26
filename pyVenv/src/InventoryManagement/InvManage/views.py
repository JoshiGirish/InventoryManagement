from django.shortcuts import render
from django.shortcuts import redirect
from .forms import *
from .models import Product
from django.core.files.storage import FileSystemStorage
import io,csv
from .filters import ProductFilter
from django.core.paginator import Paginator

def create_product_view(request):
	basic_form = ProductBasicInfoForm()
	detailed_form = ProductDetailedInfoForm()
	thumbnail_form = ProductThumbnailForm()
	storage_form = ProductStorageInfoForm()
	pricing_form = ProductPricingForm()
	status_form = ProductStatusForm()

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
		Product.objects.create(**data)
		print(request.FILES)
		uploaded_file = request.FILES['thumbnail-image']
		fs = FileSystemStorage()
		fs.save(uploaded_file.name,uploaded_file)
		return redirect('/products')
	return render(request, 'product.html',{'basic_form':basic_form,
											'thumbnail_form':thumbnail_form,
											'detailed_form':detailed_form,
											'storage_form':storage_form,
											'pricing_form':pricing_form,
											'status_form':status_form})

def products_view(request):
	products = Product.objects.all()
	# desc_filter = request.GET.get('description__contains')
	# print(request.GET)
	# print(desc_filter)
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
		print('Printing DATA:',data)
		Product.objects.filter(id=pk).update(**data)
		# prod.save()
		uploaded_file = request.FILES['thumbnail-image']
		fs = FileSystemStorage()
		fs.save(uploaded_file.name,uploaded_file)
		return redirect('/products')

	return render(request, 'product.html',{'basic_form':basic_form,
											'thumbnail_form':thumnail_form,
											'detailed_form':detailed_form,
											'storage_form':storage_form,
											'pricing_form':pricing_form,
											'status_form':status_form})

def delete_product_view(request):
	prod_id = request.POST.get('product_id')
	prod = Product.objects.get(id=prod_id)
	prod.delete()
	# if request.method == 'POST':
	# 	product = Product.objects.get(id=pk)
	return redirect('/products')

def uploadCSV(request):
	if request.method == "POST":
		csv_file = request.FILES['file']

	data_set = csv_file.read().decode('UTF-8')

	print('Starting to print data_set:',data_set)

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
		
