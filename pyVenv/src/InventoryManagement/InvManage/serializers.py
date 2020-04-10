from rest_framework import serializers

from .models import Product, Vendor, ProductPurchaseEntry

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name','category','quantity','identifier','location')

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
    class Meta:
        model = ProductPurchaseEntry
        fields = ('product','quantity','price', 'discount')

    def to_representation(self,instance):
        data = super().to_representation(instance)
        return data