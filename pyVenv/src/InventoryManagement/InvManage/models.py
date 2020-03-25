from django.db import models

class Dashboard(models.Model):
    pass
    
class Product(models.Model):
    # CATEGORY=
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
    # ProductImage = models.ImageField(upload="")
    length = models.FloatField(null=True,blank=True)
    width = models.FloatField(null=True,blank=True)
    height = models.FloatField(null=True,blank=True)
    weight = models.FloatField(null=True,blank=True)
    discount = models.IntegerField(default=0)
    image = models.ImageField(blank=True,upload_to='images/') 
    barcode = models.CharField(max_length=100,null=True,blank=True)
    expiry = models.DateTimeField(null=True, blank=True)

class Purchase(models.Model):
    VendorName = models.CharField(max_length=100)
    VendorPhone = models.CharField(max_length=10)
    VendorAdd = models.TextField()

class Sale(models.Model):
    pass
