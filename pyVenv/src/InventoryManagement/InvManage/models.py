from django.db import models

class Dashboard(models.Model):
    pass


class Vendor(models.Model):
    name = models.CharField(max_length=100)
    identifier = models.CharField(null=True, blank=True,max_length=100)
    phone = models.IntegerField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    email = models.CharField(null=True, blank=True,max_length=100)
    location = models.CharField(null=True, blank=True,max_length=100)

    def __str__(self):
        return self.name


class PurchaseOrder(models.Model):
    # Vendor details
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE)
    # Order details
    date = models.DateTimeField(null=True, blank=True)
    po = models.IntegerField()
    # Pricing information
    discount = models.FloatField()
    tax = models.FloatField()
    paid = models.FloatField()
    balance = models.FloatField()


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
    image = models.ImageField(blank=True,upload_to='images/') 
    barcode = models.CharField(max_length=100,null=True,blank=True)
    expiry = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class ProductPurchaseEntry(models.Model):
    # identifier = models.CharField(max_length=100)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField()
    price = models.FloatField()
    discount = models.FloatField()
    # subtotal = models.FloatField()
    order = models.ForeignKey(PurchaseOrder,on_delete=models.CASCADE)


class Sale(models.Model):
    pass
