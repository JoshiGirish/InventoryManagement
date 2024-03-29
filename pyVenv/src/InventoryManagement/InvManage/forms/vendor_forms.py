from django import forms

class VendorForm(forms.Form):
    """Form for basic informaion of the vendor.

    Attributes
    ----------
    name : str
        Name of the vendor.
    identifier : str
        Unique identifier of the vendor.
    gstin : str
        GSTIN number of the vendor.
    """
    prefix = "vend"
    context={
        "class": "form-control",
    }
    name = forms.CharField(widget=forms.TextInput(attrs=context))
    identifier = forms.CharField(widget=forms.TextInput(attrs=context))
    gstin = forms.CharField(label='GSTIN',widget=forms.TextInput(attrs=context))


class ShippingAddressForm(forms.Form):
    """For for shipping address.

    Attributes
    ----------
    title : str
        Title of the firm.
    name : str
        Name of the firm.
    phone : str
        Contact number of the firm.
    address : str
        Postal address.
    city : str
        City.
    state : str
        State.
    country : str
        Country.
    website : URLField
        Official website of the firm.
    post : str
        Postal code of the firm.
    """
    prefix = "ship"
    context={
        "class": "form-control",
    }
    title = forms.CharField(widget=forms.TextInput(attrs=context))
    name = forms.CharField(widget=forms.TextInput(attrs=context))
    phone = forms.CharField(widget=forms.TextInput(attrs=context))
    address = forms.CharField(label='Street', widget=forms.Textarea(
                                                    attrs={
                                                        "class": "form-control",
                                                        "rows": 3
                                                    }))
    city = forms.CharField(widget=forms.TextInput(attrs=context))
    state = forms.CharField(widget=forms.TextInput(attrs=context))
    country = forms.CharField(widget=forms.TextInput(attrs=context))
    website = forms.URLField(widget=forms.TextInput(attrs=context))
    post = forms.CharField(label='Postal Code',widget=forms.TextInput(attrs=context))
    

class CommunicationForm(forms.Form):
    """Form for communication information.

    Attributes
    ----------
    language : str
        Language of communication.
    phone : str
        Contact number of the firm.
    email : EmailField
        E-mail of the contact person.
    fax : str
        Fax number.
    """
    prefix = "com"
    context={
        "class": "form-control",
    }
    language = forms.CharField(widget=forms.TextInput(attrs=context))
    phone = forms.CharField(widget=forms.TextInput(attrs=context))
    email = forms.EmailField(widget=forms.TextInput(attrs=context))
    fax = forms.CharField(widget=forms.TextInput(attrs=context))
    

class PurchaseDataForm(forms.Form):
    """Form for purchase related data.

    Attributes
    ----------
    currency : str
        Currency of purchase.
    minorder : int
        Minimum order quantity.
    contactperson : str
        Name of the contact person.
    refcode : str
        Reference code.
    transportmode : str
        Mode of transport of the shipment.
    """
    prefix = "pdform"
    context = {
        "class": "form-control",
    }
    currency = forms.CharField(label='PO Currency',widget=forms.TextInput(attrs=context))
    minorder = forms.IntegerField(label='Min Order Qty',widget=forms.TextInput(attrs=context))
    contactperson = forms.CharField(label='Sales Person',widget=forms.TextInput(attrs=context))
    refcode = forms.CharField(label='Customer ID',widget=forms.TextInput(attrs=context))
    transportmode = forms.CharField(label='Transport Mode',widget=forms.TextInput(attrs=context))
    
    
class BankAccountForm(forms.Form):
    """Form for bank account details.

    Attributes
    ----------
    name : str
        Name of the bank.
    branch : str
        Branch number of the bank.
    region : str
        City in which the branch is located.
    route : str
        Transit number.
    number : int
        Bank account number.
    acctype : str  
        Type of bank account.
    iban : str
        IBAN number.
    code : str 
        Bank code.
    branchcode : str
        Branch code.
    """
    prefix = "bank"
    context = {
        "class": "form-control",
    }
    name = forms.CharField(label='Bank Name',widget=forms.TextInput(attrs=context))
    branch = forms.CharField(widget=forms.TextInput(attrs=context))
    region = forms.CharField(widget=forms.TextInput(attrs=context))
    route = forms.CharField(label= 'Transit Number',widget=forms.TextInput(attrs=context))
    number = forms.IntegerField(label='Account Number',widget=forms.TextInput(attrs=context))
    acctype = forms.CharField(label='Account Type',widget=forms.TextInput(attrs=context))
    iban = forms.CharField(label='IBAN Number',widget=forms.TextInput(attrs=context))
    code = forms.CharField(label='Bank Code',widget=forms.TextInput(attrs=context))
    branchcode = forms.CharField(label='Branch Code',widget=forms.TextInput(attrs=context))