from django.db import models
from django.utils import timezone


class ShippingAddress(models.Model):
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
    language = models.CharField(null=True, max_length=20, blank=True, default='English')
    phone = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True,max_length=100)
    fax = models.CharField(max_length=100, null=True, blank=True)
    

class PurchaseData(models.Model):
    currency = models.CharField(null=True, blank=True, max_length=10, verbose_name='PO Currency') # Purchase Order currency
    minorder = models.IntegerField(null=True, blank=True, verbose_name='Min Order Quantity') # Minimum order value
    contactperson = models.CharField(null=True, blank=True, max_length=50, verbose_name='Sales Person') # Sales representative of vendor company
    refcode = models.CharField(null=True, blank=True, max_length=20, verbose_name='Customer ID at Vendor') # Customer number used by the vendor for our company
    transportmode = models.CharField(null=True, blank=True, max_length=20, verbose_name='Transport Mode') # Mode of transport


class BankAccount(models.Model):
    name = models.CharField(null=True,max_length=100, verbose_name='Bank Name') # Bank name
    branch = models.CharField(null=True,max_length=20) # Bank branch
    region = models.CharField(null=True,max_length=20) # Country/region
    route = models.CharField(null=True,max_length=20, verbose_name='Transit Routing Number') # Transit routing number
    number = models.IntegerField(null=True, verbose_name='Account Number') # Bank account number
    acctype = models.CharField(null=True, blank=True, max_length=20, verbose_name='Account Type') # Type of bank account
    iban = models.CharField(null=True, blank=True, max_length=50, verbose_name='IBAN Number') # IBAN number of the bank
    code = models.CharField(null=True, blank=True, max_length= 30, verbose_name='Bank Code') # Bank code
    branchcode = models.CharField(null=True, blank=True, max_length=30, verbose_name='Branch Code') # Bank Branch code
    
    
