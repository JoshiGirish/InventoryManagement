from rest_framework import serializers

from .models import *

class ProductSerializer(serializers.ModelSerializer):
    prod_id = serializers.IntegerField(source='pk')
    class Meta:
        model = Product
        fields = ('pk','name','category','quantity','identifier','location','description','prod_id')

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

class ConsumerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consumer
        fields = ('name','identifier','phone','address','email','location')

    def to_representation(self,instance):
        data = super().to_representation(instance)
        return data


class PPEntrySerializer(serializers.ModelSerializer):
    ppe_id = serializers.IntegerField(source='pk')
    product = ProductSerializer()
    class Meta:
        model = ProductPurchaseEntry
        fields = ('ppe_id','product','quantity','price', 'discount','order')

    def to_representation(self,instance):
        data = super().to_representation(instance)
        return data

    def create(self, validated_data):
        validated_data.pop('pk')
        # print(self.data)
        prod = Product.objects.get(id=self.data['product']['prod_id'])
        validated_data['product']=prod
        return ProductPurchaseEntry.objects.create(**validated_data)

    def update(self, instance,validated_data):
        # print(instance)
        prod = Product.objects.get(id=validated_data['product']['pk'])
        instance.product = prod
        # print(validated_data)
        # instance.product = validated_data.get('product', validated_data['product'])
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


class PSEntrySerializer(serializers.ModelSerializer):
    pse_id = serializers.IntegerField(source='pk')
    product = ProductSerializer()
    class Meta:
        model = ProductSalesEntry
        fields = ('pse_id','product','quantity','price', 'discount','order')

    def to_representation(self,instance):
        data = super().to_representation(instance)
        return data

    def create(self, validated_data):
        validated_data.pop('pk')
        # print(self.data)
        prod = Product.objects.get(id=self.data['product']['prod_id'])
        validated_data['product']=prod
        return ProductSalesEntry.objects.create(**validated_data)

    def update(self, instance,validated_data):
        # print(instance)
        prod = Product.objects.get(id=validated_data['product']['pk'])
        instance.product = prod
        # print(validated_data)
        # instance.product = validated_data.get('product', validated_data['product'])
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.price = validated_data.get('price', instance.price)
        instance.discount = validated_data.get('discount', instance.discount)
        instance.order = validated_data.get('order',instance.order)
        instance.save()
        return instance
    
    
class SalesOrderSerializer(serializers.ModelSerializer):
    consumer = ConsumerSerializer()
    pses = PSEntrySerializer(source='productsalesentry_set', many=True) 

    class Meta:
        model = SalesOrder
        fields = ('consumer','date','so','subtotal','taxtotal','ordertotal','pses')

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


class PurchaseInvoiceSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    po = PurchaseOrderSerializer()
    shippingaddress = ShippingAddressSerializer()

    class Meta:
        model = PurchaseInvoice
        fields = ('company','po','shippingaddress')
        

class SalesInvoiceSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    so = SalesOrderSerializer()
    shippingaddress = ShippingAddressSerializer()
    class Meta:
        model = SalesInvoice
        fields = ('company','so','shippingaddress')
        
        
class EventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventType
        fields = ('created','updated','deleted')
        
        
class ObjectModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjectModel
        fields = ('company', 'vendor','po', 'product', 'consumer', 'so')
    
    
class HistoryFilterStateSerializer(serializers.ModelSerializer):
    events = EventTypeSerializer(source='eventtype_set', many=True)
    objModels = ObjectModelSerializer(source='objectmodel_set', many=True)
    class Meta:
        model = HistoryFilterState
        fields = ('name', 'numEntries','eventTypes', 'objModels') # using related names from nested objects
        # fields = ('name', 'numEntries','eventtype_set', 'objectmodel_set') # if related names are not defined
        
    def update(self, instance,validated_data):
        # print(instance)
        print(instance.__dict__)
        # instance.product = prod
        # # print(validated_data)
        # # instance.product = validated_data.get('product', validated_data['product'])
        # instance.quantity = validated_data.get('quantity', instance.quantity)
        # instance.price = validated_data.get('price', instance.price)
        # instance.discount = validated_data.get('discount', instance.discount)
        # instance.order = validated_data.get('order',instance.order)
        # instance.save()
        return instance