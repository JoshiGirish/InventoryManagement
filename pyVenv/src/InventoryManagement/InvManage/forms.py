from django import forms
from .models import Product

# def basic_info_form():
#     name = models.CharField(max_length=100)
#     item_type = models.CharField(max_length=100)
#     category = models.CharField(max_length=100)
#     description = models.TextField()



class ProductBasicInfoForm(forms.Form):
    prefix = "basic"
    context={
        "class": "form-control",
    }
    # Basic Information form fields
    name = forms.CharField(widget=forms.TextInput(attrs=context))
    item_type = forms.CharField(widget=forms.TextInput(attrs=context))
    category = forms.CharField(widget=forms.TextInput(attrs=context))
    description = forms.CharField(widget=forms.Textarea(
        attrs={
            "class": "form-control",
            "rows": 3
        }
    ))

class ProductDetailedInfoForm(forms.Form):
    prefix = "detailed"
    context={
        "class": "form-control",
    }
    # Dimensions form fields
    length = forms.CharField(widget=forms.TextInput(attrs=context))
    width = forms.CharField(widget=forms.TextInput(attrs=context))
    height = forms.CharField(widget=forms.TextInput(attrs=context))
    weight = forms.CharField(widget=forms.TextInput(attrs=context))


class ProductThumbnailForm(forms.Form):
    prefix = "thumbnail"
    image = forms.ImageField()
    # class Meta:
    #     model = Product
    #     fields = ['name','category','item_type','description']

    # class ProductDetailedDimensionsForm(forms.Form):

class ProductStorageInfoForm(forms.Form):
    prefix = "storage"
    barcode = forms.ImageField()
    context={
        "class": "form-control",
        "type": "date"
    }
    expiry = forms.DateField(widget=forms.widgets.DateInput(attrs=context))

class ProductPricingForm(forms.Form):
    prefix = "pricing"
    context={
        "class": "form-control",
    }
    price = forms.FloatField(label="MRP",widget=forms.NumberInput(attrs={'id': 'form_homework', 'step': "1", "class": "form-control"}))
    discount = forms.FloatField(widget=forms.NumberInput(attrs={'id': 'form_homework', 'step': "1", "class": "form-control"}))