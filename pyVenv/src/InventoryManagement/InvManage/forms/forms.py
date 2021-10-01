from django import forms
from InvManage.models import Product, Vendor, PurchaseOrder, Consumer
from django.utils import timezone

class ProductBasicInfoForm(forms.Form):
    """Form for basic product information.

    Attributes
    ----------
    name : str
        Name of the product.
    item_type : str
        Type of the product.
    category : str
        Product category.
    description : str
        Short description of the product.

    """
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
    """Form for product physical details

    Attributes
    ----------
    length : str
        Length of the product.
    width : str
        Width of the product.
    height : str
        Height of the product.
    weight : str
        Weight of the product.
    """
    prefix = "detailed"
    context={
        "class": "form-control",
    }
    # Dimensions form fields
    length = forms.CharField(widget=forms.TextInput(attrs=context))
    width = forms.CharField(widget=forms.TextInput(attrs=context))
    height = forms.CharField(widget=forms.TextInput(attrs=context))
    weight = forms.CharField(widget=forms.TextInput(attrs=context))


class ThumbnailForm(forms.Form):
    """For for product thumbnail image.

    Attributes
    ----------
    image : ImageField
        Image of the product.
    """
    prefix = "thumbnail"
    image = forms.ImageField(widget=forms.FileInput(attrs={"class": "upload"}))

class ProductStorageInfoForm(forms.Form):
    """Form for storage information.

    Attributes
    ----------
    barcode : str
        Barcode of the product.
    expiry : DateField
        Expiry date of the product.
    """
    prefix = "storage"
    barcode = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    context={
        "class": "form-control",
        "type": "date"
    }
    expiry = forms.DateField(widget=forms.widgets.DateInput(attrs=context),initial=timezone.now)

class ProductPricingForm(forms.Form):
    """Form for pricing information of the product.

    Attributes
    ----------
    price : float
        Price of the product.
    discount : float
        Default discount percentage on the product.
    """
    prefix = "pricing"
    context={
        "class": "form-control",
    }
    price = forms.FloatField(label="MRP",widget=forms.NumberInput(attrs={'id': 'form_homework', 'step': "1", "class": "form-control"}))
    discount = forms.FloatField(widget=forms.NumberInput(attrs={'id': 'form_homework', 'step': "1", "class": "form-control"}))

class ProductStatusForm(forms.Form):
    """Form for locating and identifying the product.

    Attributes
    ----------
    quantity : int
        Stock quantity of the product.
    identifier : str
        Unique identifier of the product.
    location : str
        Physical location of the product.
    """
    context={
        "class": "form-control",
    }
    prefix = "status"
    quantity = forms.IntegerField(label="Quantity", widget=forms.NumberInput(attrs={"class": "score form-control"}))
    identifier = forms.CharField(label="Identifier", widget=forms.TextInput(attrs={"class": "score form-control"}))
    location = forms.CharField(label="Location",widget=forms.TextInput(attrs={"class": "score form-control"}))

####### Purchase Order Forms #########
class PurchaseOrderBasicInfo(forms.Form):
    """Form for basic information of the purchase order.

    Attributes
    ----------
    vendor : Vendor
        Vendor associated with the purcahse order.
    date : DateField
        Date of the purchase order creation.
    po : int
        Purchase order number.
    discount : float
        Percentage of overall discount.
    tax : float
        Percentage of tax.
    paid : float
        Amount paid to the vendor.
    balance : float
        Balance amount to be paid to the vendor.
    subtotal : float
        Total of all the product purchase entries associated with the purchase order.
    taxtotal : float
        Total tax applicable on the `subtotal`.
    ordertotal : float
        Total price of the purchase order including  `taxtotal`.
    """
    prefix = "po"
    context={
        "class": "form-control",
    }
    product_choices = [(p.id, p.name) for p in Product.objects.all()]
    vendor_choices = ((v.id,v.name) for v in Vendor.objects.all())
    # Vendor details
    vendor = forms.ModelChoiceField(queryset= Vendor.objects.all(),required=True, widget=forms.Select(attrs=context))
    # Order details
    date = forms.DateField(widget=forms.widgets.DateInput(attrs={"type": "date","class":"form-control"}), initial=timezone.now)
    po = forms.IntegerField(label="PO", widget=forms.TextInput(attrs=context))
    # Pricing details
    discount = forms.FloatField(widget=forms.TextInput(attrs=context))
    tax = forms.FloatField(widget=forms.TextInput(attrs=context))
    paid = forms.FloatField(widget=forms.TextInput(attrs=context))
    balance = forms.FloatField(widget=forms.TextInput(attrs=context))
    subtotal = forms.FloatField(widget=forms.TextInput(attrs=context),initial=0.0)
    taxtotal = forms.FloatField(widget=forms.TextInput(attrs=context),initial=0.0)
    ordertotal = forms.FloatField(widget=forms.TextInput(attrs=context),initial=0.0)
    
    
####### GRN Forms #########
class GRNInfo(forms.Form):
    """Form for goods receipt note (GRN).

    Attributes
    ----------
    vendor : Vendor
        Vendor associated with the goods receipt note.
    poRef : PurchaseOrder
        List of identifiers of the purchase orders from which the goods receipt note is derived.
    identifier : str
        Unique identifier of the goods receipt note.
    date : DateField
        Date of GRN creation.
    grnType : str
        Type of GRN (``auto`` or ``manual``).
    amendNumber : int
        Amendment number of the GRN.
    amendDate : DateField
        Amendment date.
    transporter : str
        Name of the transport/shipping service.
    vehicleNumber : str
        Vehicle number using which the products are shipped.
    gateInwardNumber : str
        Gate inward number of the vehicle.
    preparedBy : str
        Name/identifier of the person who created the goods receipt note.
    checkedBy : str
        Name/identifier of the person who validated the goods receipt note.
    checkedBy : str
        Name/identifier of the person who inspected the physical products in the goods receipt note.
    approvedBy : str
        Name/identifier of the authority who approved the goods receipt note.
    """
    prefix = "grn"
    context={
        "class": "form-control",
    }
    product_choices = [(p.id, p.name) for p in Product.objects.all()]
    vendor_choices = ((v.id,v.name) for v in Vendor.objects.all())
    vendor = forms.ModelChoiceField(queryset= Vendor.objects.all(),required=True, widget=forms.Select(attrs=context))
    TYPE_CHOICES = [
        ('manual', 'Blank'),
        ('auto', 'PO Reference')
    ]
    poRef = forms.MultipleChoiceField(choices=PurchaseOrder.objects.all().values_list('pk', 'po'),label="PO References", required=False, widget=forms.SelectMultiple(attrs=context))
    identifier = forms.CharField(label="GRN Number",widget=forms.TextInput(attrs=context)) 
    date = forms.DateField(widget=forms.widgets.DateInput(attrs={"type": "date","class":"form-control"}), initial=timezone.now)
    grnType = forms.ChoiceField(choices=TYPE_CHOICES, label="Receipt Type", widget=forms.Select(attrs=context))
    amendNumber = forms.IntegerField(label="Amendment Number", widget=forms.TextInput(attrs=context))
    amendDate = forms.DateField(label="Amendment Date", widget=forms.widgets.DateInput(attrs={"type": "date","class":"form-control"}), initial=timezone.now)
    transporter = forms.CharField(label="Transporter", widget=forms.TextInput(attrs=context))
    vehicleNumber = forms.CharField(label="Vehicle Number", widget=forms.TextInput(attrs=context))
    gateInwardNumber = forms.CharField(label="Inward Number", widget=forms.TextInput(attrs=context))
    preparedBy = forms.CharField(label="Prepared By", widget=forms.TextInput(attrs=context))   
    checkedBy = forms.CharField(label="Checked By", widget=forms.TextInput(attrs=context))   
    inspectedBy = forms.CharField(label="Inspected By", widget=forms.TextInput(attrs=context))   
    approvedBy = forms.CharField(label="Approved By ", widget=forms.TextInput(attrs=context))   
    

####### Sales Order Forms #########
class SalesOrderBasicInfo(forms.Form):
    """Form for basic information on sales order.

    Attributes
    ----------
    consumer : Consumer
        Consumer associated with the sales order.
    date : DateField
        Date of the sales order creation.
    so : int
        Sales order number.
    discount : float
        Percentage discount associated with the sales order.
    tax : float
        Percentage of tax applicable.
    paid : float
        Amount received from the consumer.
    balance : float
        Amount balance with the consumer.
    subtotal : float
        Total of all the product sales entries associated with the sales order.
    taxtotal : float
        Total tax applicable on the `subtotal`.
    ordertotal : float
        Total price of the sales order including  `taxtotal`.
    """
    prefix = "so"
    context={
        "class": "form-control",
    }
    product_choices = [(p.id, p.name) for p in Product.objects.all()]
    consumer_choices = ((c.id,c.name) for c in Consumer.objects.all())
    # Vendor details
    consumer = forms.ModelChoiceField(queryset= Consumer.objects.all(),required=True, widget=forms.Select(attrs=context))
    # Order details
    date = forms.DateField(widget=forms.widgets.DateInput(attrs={"type": "date","class":"form-control"}), initial=timezone.now)
    so = forms.IntegerField(label="SO", widget=forms.TextInput(attrs=context))
    # Pricing details
    discount = forms.FloatField(widget=forms.TextInput(attrs=context))
    tax = forms.FloatField(widget=forms.TextInput(attrs=context))
    paid = forms.FloatField(widget=forms.TextInput(attrs=context))
    balance = forms.FloatField(widget=forms.TextInput(attrs=context))
    subtotal = forms.FloatField(widget=forms.TextInput(attrs=context),initial=0.0)
    taxtotal = forms.FloatField(widget=forms.TextInput(attrs=context),initial=0.0)
    ordertotal = forms.FloatField(widget=forms.TextInput(attrs=context),initial=0.0)

    
class ConsumerForm(forms.Form):
    """Form for consumer.

    Attributes
    ----------
    name : str
        Name of the consumer.
    identifier : str
        Unique identifier of the consumer.
    gstin : str
        GSTIN number of the consumer.
    phone : str
        Contact number.
    address : str
        Address of the consumer.
    email : str
        E-mail address of the consumer.
    location : str
        City of the consumer.
    """
    prefix = "consumer"
    context={
        "class": "form-control",
    }
    name = forms.CharField(widget=forms.TextInput(attrs=context))
    identifier = forms.CharField(widget=forms.TextInput(attrs=context))
    gstin = forms.CharField(label='GSTIN',widget=forms.TextInput(attrs=context))
    phone = forms.CharField(widget=forms.TextInput(attrs=context))
    address = forms.CharField(widget=forms.Textarea(
        attrs={
            "class": "form-control",
            "rows": 3
        }
    ))
    email = forms.CharField(widget=forms.TextInput(attrs=context))
    location = forms.CharField(widget=forms.TextInput(attrs=context))


class GRNEntryForm(forms.Form):
    """Form for goods receipt note entry (GRNE).

    Attributes
    ----------
    product : Product
        Product associated with the goods receipt note entry.
    grne_id : int
        Unique identifier of the GRNE.
    ppe_id : int
        Unique identifier of the product purchase entry associated with the GRNE.
    quantity : int
        Ordered quantity of product with reference to product purchase entry.
    remark : str
        Remarks of the quality engineer or the GRN creator about status of products received.
    receivedQty : str
        Quantity of product received against the ordered quantity.
    acceptedQty : str
        Quantity of product accepted as OK.
    rejectedQty : str
        Quantity of product rejected (not OK, on HOLD, extra delivery, etc.)
    """
    prefix = "form"
    context = {
        "class": "form-control",
    }
    product = forms.ModelChoiceField(
                    queryset= Product.objects.all(),
                    widget=forms.Select(attrs={
                                            "class": "form-control",
                                            "onchange":"setIdentifier(this)"}))
    grne_id = forms.IntegerField(widget=forms.TextInput(attrs={"value":""}))
    ppe_id = forms.IntegerField(widget=forms.TextInput(attrs=context), required=False)
    quantity = forms.IntegerField(widget=forms.TextInput(attrs=context))
    remark = forms.CharField(widget=forms.TextInput(attrs=context), required=False)
    receivedQty = forms.CharField(widget=forms.TextInput(attrs=context))
    acceptedQty = forms.CharField(widget=forms.TextInput(attrs=context))
    rejectedQty = forms.CharField(widget=forms.TextInput(attrs=context))
    

class ProductPurchaseEntryForm(forms.Form):
    """Form for product purchase entry.

    Attributes
    ----------
    ppe_id : int
        Unique identifier of the product purchase entry.
    product : Product
        Product associated wit the product purchase entry.
    quantity : int
        Quantity of the product to be ordered.
    price : float
        Price of the product.
    discount : float
        Percentage discount on the product purchase.
    """
    prefix = "form"
    context={
        "class": "form-control",
    }
    # product_choices = [(p.id, p.name) for p in Product.objects.all()]
    ppe_id = forms.IntegerField(widget=forms.TextInput(attrs={"value":""}))
    product = forms.ModelChoiceField(
                    queryset= Product.objects.all(),
                    widget=forms.Select(attrs={
                                            "class": "form-control",
                                            "onchange":"setIdentifier(this)"}))
    # identifier = forms.CharField(widget=forms.)
    quantity = forms.IntegerField(widget=forms.TextInput(attrs=context))
    price = forms.FloatField(widget=forms.TextInput(attrs=context))
    discount = forms.FloatField(widget=forms.TextInput(attrs=context))
    
    
class ProductSalesEntryForm(forms.Form):
    """Form for product sales entry.

    Attributes
    ----------
    pse_id : int
        Unique identifier of the product sales entry.
    product : Product
        Product associated with the product sales entry.
    quantity : int
        Quantity of the product.
    price : float
        Price of the product.
    discount : float
        Percentage discount on the product.
    """
    prefix = "form"
    context={
        "class": "form-control",
    }
    # product_choices = [(p.id, p.name) for p in Product.objects.all()]
    pse_id = forms.IntegerField(widget=forms.TextInput(attrs={"value":""}))
    product = forms.ModelChoiceField(
                    queryset= Product.objects.all(),
                    widget=forms.Select(attrs={
                                            "class": "form-control",
                                            "onchange":"setIdentifier(this)"}))
    # identifier = forms.CharField(widget=forms.)
    quantity = forms.IntegerField(widget=forms.TextInput(attrs=context))
    price = forms.FloatField(widget=forms.TextInput(attrs=context))
    discount = forms.FloatField(widget=forms.TextInput(attrs=context))
    

class CompanyForm(forms.Form):
    """Form for company.

    Attributes
    ----------
    name : str
        Name of the company.
    owner : str
        Name of the owner of the company.
    gstin : str
        GSTIN number of the company.
    phone : str
        Contact number of the company.
    address : str
        Postal address.
    email : str
        E-mail address of the contact person.
    location : str
        City of the company.
    """
    prefix = "comp"
    context={
        "class": "form-control",
    }
    name = forms.CharField(widget=forms.TextInput(attrs=context))
    owner = forms.CharField(widget=forms.TextInput(attrs=context))
    gstin = forms.CharField(label='GSTIN',widget=forms.TextInput(attrs=context))
    phone = forms.CharField(widget=forms.TextInput(attrs=context))
    address = forms.CharField(widget=forms.Textarea(
        attrs={
            "class": "form-control",
            "rows": 3
        }
    ))
    email = forms.CharField(widget=forms.TextInput(attrs=context))
    location = forms.CharField(widget=forms.TextInput(attrs=context))


    
class HistoryForm(forms.Form):
    """Form for history view.

    Attributes
    ----------
    qlen : int
        Count of the events visible on the history view.
    """
    prefix = 'history'
    context={
        "class": "form-control",
    }
    qlen = forms.IntegerField(widget=forms.TextInput(attrs=context))