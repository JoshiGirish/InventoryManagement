from django.shortcuts import render
from .forms import *

def product_view(request):
	basic_form = ProductBasicInfoForm()
	detailed_form = ProductDetailedInfoForm()
	thumnail_form = ProductThumbnailForm()
	storage_form = ProductStorageInfoForm()
	pricing_form = ProductPricingForm()
	return render(request, 'product.html',{'basic_form':basic_form,
											'thumbnail_form':thumnail_form,
											'detailed_form':detailed_form,
											'storage_form':storage_form,
											'pricing_form':pricing_form})
