from django.db import models

class Dashboard(models.Model):
    
    
    
    
class Product(models.Model):
    CATEGORY=
    ProductName = models.CharField(max_length=50)
    ProductCategory = models.CharField(choice=CATEGORY,)
    ProductPrice = models.FloatField()
    ProductQuantity = models.IntegerField()
    ProductImage = models.ImageField(upload=)
    ProductLength = models.FloatField()
    ProductWidth = models.FloatField()
    ProductHeight = models.FloatField()
    ProductDescription = models.TextField()



class Purchase(models.Model):
    VendorName = models.CharField(max_length=100)
    VendorPhone = models.CharField(max_legnth=10)
    VendorAdd = models.TextField()





class Sale(models.Model):

