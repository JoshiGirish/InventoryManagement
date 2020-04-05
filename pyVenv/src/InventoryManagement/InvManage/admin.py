from django.contrib import admin
from .models import Product, PurchaseOrder, Vendor

admin.site.register(Product)
admin.site.register(PurchaseOrder)
admin.site.register(Vendor)
