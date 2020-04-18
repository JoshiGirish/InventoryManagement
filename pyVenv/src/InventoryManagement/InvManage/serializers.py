from rest_framework import serializers

from .models import Product, Vendor, ProductPurchaseEntry, PurchaseOrder, Company, Invoice, ShippingAddress

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('pk','name','category','quantity','identifier','location','description')

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
    # product = ProductSerializer()
    ppe_id = serializers.IntegerField(source='pk')
    class Meta:
        model = ProductPurchaseEntry
        fields = ('ppe_id','product','quantity','price', 'discount','order')

    def to_representation(self,instance):
        data = super().to_representation(instance)
        return data

    def create(self, validated_data):
        validated_data.pop('pk')
        print(validated_data)
        return ProductPurchaseEntry.objects.create(**validated_data)

    def update(self, instance,validated_data):
        print(validated_data)
        instance.product = validated_data.get('product', instance.product)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.price = validated_data.get('price', instance.price)
        instance.discount = validated_data.get('discount', instance.discount)
        instance.order = validated_data.get('order',instance.order)
        instance.save()
        return instance

class PurchaseOrderSerializer(serializers.ModelSerializer):
    vendor = VendorSerializer()
    ppes = PPEntrySerializer(source='productpurchaseentry_set', many=True) 

    class Meta:
        model = PurchaseOrder
        fields = ('vendor','date','po','subtotal','taxtotal','ordertotal','ppes')

    def to_representation(self,instance):
        data = super().to_representation(instance)
        return data

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('name','owner','phone','address','email','location','image')

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