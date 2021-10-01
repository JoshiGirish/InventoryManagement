from django.db import models
from django.utils import timezone


class ShippingAddress(models.Model):
    """Model of the shipping address.

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
    title = models.CharField(null=True,max_length=20) # Company, Ms./, ...
    name = models.CharField(max_length=100) 
    phone = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(null=True, blank=True, verbose_name='Street') # House/Street number
    city = models.CharField(null=True, blank=True,max_length=100)
    state = models.CharField(null=True, max_length=30)
    country = models.CharField(null=True, max_length=30)
    website = models.URLField(null=True, blank=True,max_length=100)
    post = models.CharField(null=True, max_length=20, verbose_name='Postal Code')
    
    
class Communication(models.Model):
    """Model of the communication information.

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
    language = models.CharField(null=True, max_length=20, blank=True, default='English')
    phone = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True,max_length=100)
    fax = models.CharField(max_length=100, null=True, blank=True)
    

class PurchaseData(models.Model):
    """Model of the purchase data.

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
    currency = models.CharField(null=True, blank=True, max_length=10, verbose_name='PO Currency') # Purchase Order currency
    minorder = models.IntegerField(null=True, blank=True, verbose_name='Min Order Quantity') # Minimum order value
    contactperson = models.CharField(null=True, blank=True, max_length=50, verbose_name='Sales Person') # Sales representative of vendor company
    refcode = models.CharField(null=True, blank=True, max_length=20, verbose_name='Customer ID at Vendor') # Customer number used by the vendor for our company
    transportmode = models.CharField(null=True, blank=True, max_length=20, verbose_name='Transport Mode') # Mode of transport


class BankAccount(models.Model):
    """Model of the bank account details.

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
    name = models.CharField(null=True,max_length=100, verbose_name='Bank Name') # Bank name
    branch = models.CharField(null=True,max_length=20) # Bank branch
    region = models.CharField(null=True,max_length=20) # Country/region
    route = models.CharField(null=True,max_length=20, verbose_name='Transit Routing Number') # Transit routing number
    number = models.IntegerField(null=True, verbose_name='Account Number') # Bank account number
    acctype = models.CharField(null=True, blank=True, max_length=20, verbose_name='Account Type') # Type of bank account
    iban = models.CharField(null=True, blank=True, max_length=50, verbose_name='IBAN Number') # IBAN number of the bank
    code = models.CharField(null=True, blank=True, max_length= 30, verbose_name='Bank Code') # Bank code
    branchcode = models.CharField(null=True, blank=True, max_length=30, verbose_name='Branch Code') # Bank Branch code
    
    
