from django.db import models

class Dashboard(models.Model):
    pass
    
    
    
class Product(models.Model):
    # CATEGORY=
    # Basic Information
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    item_type = models.CharField(max_length=100)
    description = models.TextField()
    # Pricing
    price = models.FloatField()
    quantity = models.IntegerField(default=0,null=True)
    # Dimensions
    # ProductImage = models.ImageField(upload="")
    length = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()
    weight = models.FloatField()
    discount = models.IntegerField(default=0)
    product_image = models.ImageField(upload_to='images/') 




class Purchase(models.Model):
    VendorName = models.CharField(max_length=100)
    VendorPhone = models.CharField(max_length=10)
    VendorAdd = models.TextField()





class Sale(models.Model):
    pass
