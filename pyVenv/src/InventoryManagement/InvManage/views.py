from django.shortcuts import render
from .forms import *
from .models import Product
from django.core.files.storage import FileSystemStorage

def product_view(request):
	basic_form = ProductBasicInfoForm()
	detailed_form = ProductDetailedInfoForm()
	thumnail_form = ProductThumbnailForm()
	storage_form = ProductStorageInfoForm()
	pricing_form = ProductPricingForm()

	if request.method == 'POST':
		types = [ProductBasicInfoForm, ProductDetailedInfoForm, ProductThumbnailForm, ProductStorageInfoForm, ProductPricingForm]
		# types = [basic_form, detailed_form, thumnail_form, storage_form, pricing_form]
		data = {}
		for form_type in types:
			pre = form_type.prefix
			form = form_type(request.POST, prefix = pre)
			if form.is_valid():
				data.update(form.cleaned_data)
		Product.objects.create(**data)
		uploaded_file = request.FILES['thumbnail-image']
		fs = FileSystemStorage()
		fs.save(uploaded_file.name,uploaded_file)
		# print('Printing POST: ', request.POST)
		# for pre in prefixes:
		# 	form = ProductDetailedInfoForm(request.POST, prefix = "detailed")
		# 	print('Printing Detailed form: ', dimensions_form)
		# 	print(dimensions_form.cleaned_data)
		# print('Length: ', dimensions_form.fields["length"].value)
		# if dimensions_form.is_valid():
		# 	dimensions_form.save()
	return render(request, 'product.html',{'basic_form':basic_form,
											'thumbnail_form':thumnail_form,
											'detailed_form':detailed_form,
											'storage_form':storage_form,
											'pricing_form':pricing_form})
