from django.shortcuts import render
from django.shortcuts import redirect
from .forms import *
from .models import Product
from django.core.files.storage import FileSystemStorage

def create_product_view(request):
	basic_form = ProductBasicInfoForm()
	detailed_form = ProductDetailedInfoForm()
	thumnail_form = ProductThumbnailForm()
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

def products_view(request):
	products = Product.objects.all()
	return render(request, 'display/products.html',{'products': products})

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
		
