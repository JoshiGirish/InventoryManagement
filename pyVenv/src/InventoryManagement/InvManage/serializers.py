from rest_framework import serializers

from .models import Product, Vendor, ProductPurchaseEntry, PurchaseOrder, Company, Invoice, ShippingAddress

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name','category','quantity','identifier','location','description')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ('name','identifier','phone','address','email','location')

    def to_representation(self,instance):
        data = super().to_representation(instance)
        return data

class PPEntrySerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = ProductPurchaseEntry
        fields = ('product','quantity','price', 'discount')

    def to_representation(self,instance):
        data = super().to_representation(instance)
        return data

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('name','owner','phone','address','email','location','image')

class PurchaseOrderSerializer(serializers.ModelSerializer):
    vendor = VendorSerializer()
    ppes = PPEntrySerializer(source='productpurchaseentry_set', many=True) 

    class Meta:
        model = PurchaseOrder
        fields = ('vendor','date','po','subtotal','taxtotal','ordertotal','ppes')

    def to_representation(self,instance):
        data = super().to_representation(instance)
        return data

class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = ('name','address','phone','email','location')


class InvoiceSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    po = PurchaseOrderSerializer()
    shippingaddress = ShippingAddressSerializer()

    class Meta:
        model = Invoice
        fields = ('company','po','shippingaddress')