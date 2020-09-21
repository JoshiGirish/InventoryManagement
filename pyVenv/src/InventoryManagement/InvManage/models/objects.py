from django.db import models
from django.utils import timezone
from .reuse import ShippingAddress, Communication, BankAccount, PurchaseData


class Dashboard(models.Model):
    pass


class Company(models.Model):
    name = models.CharField(null=True,max_length=100)
    owner = models.CharField(null=True,max_length=100)
    phone = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    email = models.CharField(null=True, blank=True,max_length=100)
    location = models.CharField(null=True, blank=True,max_length=100)
    image = models.ImageField(blank=True,upload_to='images/') 
    shippingaddress = models.OneToOneField(ShippingAddress,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return self.name


class Vendor(models.Model):
    name = models.CharField(max_length=100)
    identifier = models.CharField(null=True, blank=True,max_length=100)
    address = models.OneToOneField(ShippingAddress, on_delete=models.PROTECT, null=True)
    communication = models.OneToOneField(Communication, on_delete=models.PROTECT, null=True)
    bankaccount = models.OneToOneField(BankAccount, on_delete=models.PROTECT, null=True)
    purchasedata = models.OneToOneField(PurchaseData, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.name

class Consumer(models.Model):
    name = models.CharField(max_length=100)
    identifier = models.CharField(null=True, blank=True,max_length=100)
    phone = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    email = models.CharField(null=True, blank=True,max_length=100)
    location = models.CharField(null=True, blank=True,max_length=100)

    def __str__(self):
        return self.name

class PurchaseOrder(models.Model):
    # Vendor details
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE)
    # Order details
    date = models.DateTimeField(default=timezone.now,null=True, blank=True)
    po = models.IntegerField()
    # Pricing information
    discount = models.FloatField(default=0,null=True)
    tax = models.FloatField(default=0,null=True)
    paid = models.FloatField(default=0,null=True)
    balance = models.FloatField(default=0,null=True)
    subtotal = models.FloatField(default=0,null=True)
    taxtotal = models.FloatField(default=0,null=True)
    ordertotal = models.FloatField(default=0,null=True)


class SalesOrder(models.Model):
    # Vendor details
    consumer = models.ForeignKey(Consumer,on_delete=models.CASCADE)
    # Order details
    date = models.DateTimeField(default=timezone.now,null=True, blank=True)
    so = models.IntegerField()
    # Pricing information
    discount = models.FloatField(default=0,null=True)
    tax = models.FloatField(default=0,null=True)
    paid = models.FloatField(default=0,null=True)
    balance = models.FloatField(default=0,null=True)
    subtotal = models.FloatField(default=0,null=True)
    taxtotal = models.FloatField(default=0,null=True)
    ordertotal = models.FloatField(default=0,null=True)


class Product(models.Model):
    # Basic Information
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    item_type = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    # Pricing
    price = models.FloatField(null=True,blank=True)
    quantity = models.IntegerField(default=0,null=True)
    identifier = models.CharField(max_length=30,blank=False, null=True)
    location = models.CharField(max_length=100,blank=False, null=True)
    # Dimensions
    length = models.FloatField(null=True,blank=True)
    width = models.FloatField(null=True,blank=True)
    height = models.FloatField(null=True,blank=True)
    weight = models.FloatField(null=True,blank=True)
    discount = models.IntegerField(default=0)
    barcode = models.CharField(max_length=100,null=True,blank=True)
    expiry = models.DateTimeField(null=True, blank=True)
    image = models.ImageField(blank=True,upload_to='images/') 

    def __str__(self):
        return self.name


class ProductPurchaseEntry(models.Model):
    # identifier = models.CharField(max_length=100)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField(null=True)
    price = models.FloatField(null=True)
    discount = models.FloatField(null=True)
    # subtotal = models.FloatField()
    order = models.ForeignKey(PurchaseOrder,on_delete=models.CASCADE)


class ProductSalesEntry(models.Model):
    # identifier = models.CharField(max_length=100)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField(null=True)
    price = models.FloatField(null=True)
    discount = models.FloatField(null=True)
    # subtotal = models.FloatField()
    order = models.ForeignKey(SalesOrder,on_delete=models.CASCADE)


class PurchaseInvoice(models.Model):
    company = models.OneToOneField(Company,on_delete=models.SET_NULL,null=True)
    po = models.OneToOneField(PurchaseOrder,on_delete=models.SET_NULL,null=True)
    shippingaddress = models.OneToOneField(ShippingAddress,on_delete=models.SET_NULL,null=True)
    communication = models.OneToOneField(Communication, on_delete=models.SET_NULL, null=True)
    
    
class SalesInvoice(models.Model):
    company = models.OneToOneField(Company,on_delete=models.SET_NULL,null=True)
    so = models.OneToOneField(SalesOrder,on_delete=models.SET_NULL,null=True)
    shippingaddress = models.OneToOneField(ShippingAddress,on_delete=models.SET_NULL,null=True)
