from django import forms
from .models import Product, Vendor


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
    image = forms.ImageField(widget=forms.FileInput(attrs={"class": "upload"}))
    # class Meta:
    #     model = Product
    #     fields = ['name','category','item_type','description']

    # class ProductDetailedDimensionsForm(forms.Form):

class ProductStorageInfoForm(forms.Form):

    prefix = "storage"
    barcode = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
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

class ProductStatusForm(forms.Form):
    context={
        "class": "form-control",
    }
    prefix = "status"
    quantity = forms.IntegerField(label="Quantity", widget=forms.NumberInput(attrs={"class": "score form-control"}))
    identifier = forms.CharField(label="Identifier", widget=forms.TextInput(attrs={"class": "score form-control"}))
    location = forms.CharField(label="Location",widget=forms.TextInput(attrs={"class": "score form-control"}))

####### Purchase Order Forms #########

class PurchaseOrderBasicInfo(forms.Form):
    prefix = "po"
    context={
        "class": "form-control",
    }
    product_choices = [(p.id, p.name) for p in Product.objects.all()]
    vendor_choices = [(v.id, v.name) for v in Vendor.objects.all()]

    # Vendor details
    vendor = forms.ChoiceField(required=True, label='Vendors', choices=vendor_choices)
    
    # Order details
    date = forms.DateField(widget=forms.widgets.DateInput(attrs={"type": "date","class":"form-control"}))
    po = forms.IntegerField(label="PO", widget=forms.TextInput(attrs=context))
    # Pricing details
    discount = forms.FloatField(widget=forms.TextInput(attrs=context))
    tax = forms.FloatField(widget=forms.TextInput(attrs=context))
    paid = forms.FloatField(widget=forms.TextInput(attrs=context))
    balance = forms.FloatField(widget=forms.TextInput(attrs=context))
    # prods = forms.ChoiceField(required=True, label='Products', choices=product_choices)
    
class VendorForm(forms.Form):
    prefix = "vend"
    context={
        "class": "form-control",
    }
    name = forms.CharField(widget=forms.TextInput(attrs=context))
    identifier = forms.CharField(widget=forms.TextInput(attrs=context))
    phone = forms.IntegerField(widget=forms.TextInput(attrs=context))
    address = forms.CharField(widget=forms.Textarea(
        attrs={
            "class": "form-control",
            "rows": 3
        }
    ))
    email = forms.CharField(widget=forms.TextInput(attrs=context))
    location = forms.CharField(widget=forms.TextInput(attrs=context))


class ProductPurchaseEntryForm(forms.Form):
    prefix = "form"
    context={
        "class": "form-control",
    }
    product_choices = [(p.id, p.name) for p in Product.objects.all()]
    product = forms.ChoiceField(required=True, label='Products', choices=product_choices)
    # identifier = forms.CharField(widget=forms.)
    quantity = forms.IntegerField(widget=forms.TextInput(attrs=context))
    price = forms.FloatField(widget=forms.TextInput(attrs=context))
    discount = forms.FloatField(widget=forms.TextInput(attrs=context))
    