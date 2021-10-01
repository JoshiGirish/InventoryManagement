from rest_framework import serializers

from .models import *


class ShippingAddressSerializer(serializers.ModelSerializer):
    """Serializer for ``ShippingAddress`` class instance.

        The ``ShippingAddressSerializer.data`` attribute gives the ``JSON`` serialized data of the ``ShippingAddress`` instance::
        
            {
                "name": "Harding Gross",
                "address": "8798 At, St., 7639",
                "city": "Rome",
                "phone": "936 651-4847",
                "state": "Lazio",
                "country": "Italy",
                "post": "300326"
            }
    
    """
    class Meta:
        model = ShippingAddress
        fields = ('name','address','city','phone','state','country','post')


class CommunicationSerializer(serializers.ModelSerializer):
    """Serializer for ``Communication`` class instance.

        The ``CommunicationSerializer.data`` attribute gives the ``JSON`` serialized data of the ``Communication`` instance::
        
            {
                "email": "JohnDoe@domain.com",
                "phone": "(332) 654 6432"
            }
    
    """
    class Meta:
        model = Communication
        fields = ('email','phone')


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for ``Product`` class instance.

        The ``ProductSerializer.data`` attribute gives the ``JSON`` serialized data of the ``Product`` instance::
        
            {
                "pk": 637,
                "name": "Piano",
                "category": "Ultricies PC",
                "quantity": 23921,
                "identifier": "PROD9",
                "location": "Musselburgh",
                "description": "88-key, Tri-sensor Scaled Hammer Action Keyboard II, Simulated ebony and ivory keys ",
                "prod_id": 637
            }
    
    """
    prod_id = serializers.IntegerField(source='pk')
    class Meta:
        model = Product
        fields = ('pk','name','category','quantity','identifier','location','description','prod_id')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data


class VendorSerializer(serializers.ModelSerializer):
    """Serializer for ``Vendor`` class instance.

        The ``VendorSerializer.data`` attribute gives the ``JSON`` serialized data of the ``Vendor`` instance::
        
            {
                "name": "Harding Gross",
                "identifier": "HG",
                "gstin": "89ACC16843543",
                "address": {
                    "name": "Harding Gross",
                    "address": "8798 At, St., 7639",
                    "city": "Rome",
                    "phone": "936 651-4847",
                    "state": "Lazio",
                    "country": "Italy",
                    "post": "300326"
            }
    
    """
    address = ShippingAddressSerializer()
    class Meta:
        model = Vendor
        fields = ('name','identifier','gstin','address')
        phone = serializers.IntegerField(source='communication__phone')
        email = serializers.IntegerField(source='communication__email')

    def to_representation(self,instance):
        data = super().to_representation(instance)
        return data


class ConsumerSerializer(serializers.ModelSerializer):
    """Serializer for ``Consumer`` class instance.

        The ``ConsumerSerializer.data`` attribute gives the ``JSON`` serialized data of the ``Consumer`` instance::
        
            {
                "name": "The Music Store",
                "identifier": "CONS1256",
                "gstin": "89AAC4633353643",
                "phone": "+91 8325642358",
                "address": "Plot no 958, N- 4, Neo Complex, Barh, Wokha, Nagaland, 797111",
                "email": "JohnDoe@themusic.store",
                "location": "Wokha"
            }
    
    """
    class Meta:
        model = Consumer
        fields = ('name','identifier','gstin','phone','address','email','location')

    def to_representation(self,instance):
        data = super().to_representation(instance)
        return data


class PPEntrySerializer(serializers.ModelSerializer):
    """Serializer for ``ProductPurchaseEntry`` class instance.

        The ``PPEntrySerializer.data`` attribute gives the ``JSON`` serialized data of the ``ProductPurchaseEntry`` instance::
        
            {
                "ppe_id": 324,
                "product": {
                    "pk": 637,
                    "name": "Piano",
                    "category": "Ultricies PC",
                    "quantity": 23921,
                    "identifier": "PROD9",
                    "location": "Musselburgh",
                    "description": "88-key, Tri-sensor Scaled Hammer Action Keyboard II, Simulated ebony and ivory keys ",
                    "prod_id": 637
                },
                "quantity": 100,
                "price": 10.0,
                "discount": 0.0,
                "order": 182,
                "pendingQty": 50
            }
    
    """
    ppe_id = serializers.IntegerField(source='pk')
    product = ProductSerializer()
    pendingQty = serializers.ReadOnlyField(source='pending_quantity')
    class Meta:
        model = ProductPurchaseEntry
        fields = ('ppe_id','product','quantity','price', 'discount','order','pendingQty')
        # read_only_fields = ['pendingQty']

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
    """Serializer for ``PurchaseOrder`` class instance.

        The ``PurchaseOrderSerializer.data`` attribute gives the ``JSON`` serialized data of the ``PurchaseOrder`` instance::
        
            {
                "vendor": {
                    "name": "Girish",
                    "identifier": "GJ",
                    "gstin": "GSTIN002",
                    "address": {
                        "name": "alsf",
                        "address": "jas;k",
                        "city": ";sdalkf",
                        "phone": "alsf",
                        "state": "kjdflk",
                        "country": "ljflkj",
                        "post": "54545"
                    }
                },
                "date": "25-Sep-2021",
                "po": 293,
                "subtotal": 279975.0,
                "taxtotal": 22398.0,
                "ordertotal": 302373.0,
                "ppes": [
                    {
                        "ppe_id": 324,
                        "product": {
                            "pk": 637,
                            "name": "piano",
                            "category": "Ultricies PC",
                            "quantity": 23921,
                            "identifier": "PROD9",
                            "location": "Musselburgh",
                            "description": "88-key, Tri-sensor Scaled Hammer Action Keyboard II, Simulated ebony and ivory keys ",
                            "prod_id": 637
                        },
                        "quantity": 100,
                        "price": 10.0,
                        "discount": 0.0,
                        "order": 182,
                        "pendingQty": 50
                    },
                    {
                        "ppe_id": 325,
                        "product": {
                            "pk": 645,
                            "name": "Tabl",
                            "category": "Sociis Natoque Company",
                            "quantity": 38276,
                            "identifier": "PROD17",
                            "location": "Schagen",
                            "description": "aldgjlakjlkasdj",
                            "prod_id": 645
                        },
                        "quantity": 250,
                        "price": 90.0,
                        "discount": 8.0,
                        "order": 182,
                        "pendingQty": 70
                    },
                    {
                        "ppe_id": 326,
                        "product": {
                            "pk": 638,
                            "name": "Goblet drum",
                            "category": "Est Congue Consulting",
                            "quantity": 46076,
                            "identifier": "PROD10",
                            "location": "Kaluga",
                            "description": "aldgjlakjlkasdj",
                            "prod_id": 638
                        },
                        "quantity": 200,
                        "price": 150.0,
                        "discount": 12.0,
                        "order": 182,
                        "pendingQty": 200
                    }
                ]
            }
    
    """
    vendor = VendorSerializer()
    ppes = PPEntrySerializer(source='productpurchaseentry_set', many=True)
    date = serializers.DateTimeField(format="%d-%b-%Y")

    class Meta:
        model = PurchaseOrder
        fields = ('vendor','date','po','subtotal','taxtotal','ordertotal','ppes')

    def to_representation(self,instance):
        data = super().to_representation(instance)
        return data
    

class GRNEntrySerializer(serializers.ModelSerializer):
    """Serializer for ``GRNEntry`` class instance.

        The ``GRNEntrySerializer.data`` attribute gives the ``JSON`` serialized data of the ``GRNEntry`` instance::
        
            {
                "grn": 103,
                "grne_id": 117,
                "product": {
                    "pk": 637,
                    "name": "piano",
                    "category": "Ultricies PC",
                    "quantity": 23921,
                    "identifier": "PROD9",
                    "location": "Musselburgh",
                    "description": "88-key, Tri-sensor Scaled Hammer Action Keyboard II, Simulated ebony and ivory keys ",
                    "prod_id": 637
                },
                "quantity": 100,
                "receivedQty": 50,
                "acceptedQty": 50,
                "rejectedQty": 0,
                "remark": "OK"
            }
    
    """
    grne_id = serializers.IntegerField(source='pk')
    product = ProductSerializer()
    grn = serializers.IntegerField(source='grn.pk')
    class Meta:
        model = GRNEntry
        fields = ('grn','grne_id','product','quantity','receivedQty', 'acceptedQty','rejectedQty','remark')

    def to_representation(self,instance):
        data = super().to_representation(instance)
        return data

    def create(self, validated_data):
        validated_data.pop('pk')
        print('\n\n\n')
        print(self.data)
        print('\n\n\n')
        prod = Product.objects.get(id=self.data['product']['prod_id'])
        validated_data['product']=prod
        grn = GoodsReceiptNote.objects.get(id=self.data['grn'])
        validated_data['grn']=grn
        return GRNEntry.objects.create(**validated_data)
    
    def update(self, instance,validated_data):
        prod = Product.objects.get(id=validated_data['product']['pk'])
        instance.product = prod
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.receivedQty = validated_data.get('receivedQty', instance.receivedQty)
        instance.acceptedQty = validated_data.get('acceptedQty', instance.acceptedQty)
        instance.rejectedQty = validated_data.get('rejectedQty',instance.rejectedQty)
        instance.remark = validated_data.get('remark',instance.remark)
        instance.save()
        return instance
    
    
class GRNEntryWithPORefSerializer(serializers.ModelSerializer):
    """Serializer for ``GRNEntry`` class instance if the GRN references a purchase order.

        The ``GRNEntryWithPORefSerializer.data`` attribute gives the ``JSON`` serialized data of the ``GRNEntry`` instance::
        
            {
                "grn": 103,
                "grne_id": 117,
                "ppe_id": 324,
                "po_id": 293,
                "product": {
                    "pk": 637,
                    "name": "piano",
                    "category": "Ultricies PC",
                    "quantity": 23921,
                    "identifier": "PROD9",
                    "location": "Musselburgh",
                    "description": "88-key, Tri-sensor Scaled Hammer Action Keyboard II, Simulated ebony and ivory keys ",
                    "prod_id": 637
                },
                "quantity": 100,
                "receivedQty": 50,
                "acceptedQty": 50,
                "rejectedQty": 0,
                "remark": "OK"
            }
    
    """
    grne_id = serializers.IntegerField(source='pk')
    ppe_id = serializers.IntegerField(source='ppes.pk')
    po_id = serializers.IntegerField(source='ppes.order.po')
    product = ProductSerializer()
    grn = serializers.IntegerField(source='grn.pk')
    class Meta:
        model = GRNEntry
        fields = ('grn','grne_id','ppe_id','po_id','product','quantity','receivedQty', 'acceptedQty','rejectedQty','remark')

    def to_representation(self,instance):
        data = super().to_representation(instance)
        return data

    def create(self, validated_data):
        validated_data.pop('pk')
        prod = Product.objects.get(id=self.data['product']['prod_id'])
        validated_data['product']=prod
        grn = GoodsReceiptNote.objects.get(id=self.data['grn'])
        validated_data['grn']=grn
        ppe = ProductPurchaseEntry.objects.get(id=self.data['ppe_id'])
        validated_data['ppes']=ppe
        return GRNEntry.objects.create(**validated_data)

    def update(self, instance,validated_data):
        prod = Product.objects.get(id=validated_data['product']['pk'])
        instance.product = prod
        instance.quantity = int(validated_data.get('quantity', instance.quantity))
        instance.receivedQty = int(validated_data.get('receivedQty', instance.receivedQty))
        instance.acceptedQty = int(validated_data.get('acceptedQty', instance.acceptedQty))
        instance.rejectedQty = int(validated_data.get('rejectedQty',instance.rejectedQty))
        instance.remark = validated_data.get('remark',instance.remark)
        instance.save()
        return instance
    

class GoodsReceiptNoteSerializer(serializers.ModelSerializer):
    """Serializer for ``GoodsReceiptNote`` class instance.

        The ``GoodsReceiptNoteSerializer.data`` attribute gives the ``JSON`` serialized data of the ``GoodsReceiptNote`` instance::
        
            {
                "grnes": [
                    {
                        "grn": 103,
                        "grne_id": 117,
                        "ppe_id": 324,
                        "po_id": 293,
                        "product": {
                            "pk": 637,
                            "name": "piano",
                            "category": "Ultricies PC",
                            "quantity": 23921,
                            "identifier": "PROD9",
                            "location": "Musselburgh",
                            "description": "88-key, Tri-sensor Scaled Hammer Action Keyboard II, Simulated ebony and ivory keys ",
                            "prod_id": 637
                        },
                        "quantity": 100,
                        "receivedQty": 50,
                        "acceptedQty": 50,
                        "rejectedQty": 0,
                        "remark": "OK"
                    },
                    {
                        "grn": 103,
                        "grne_id": 118,
                        "ppe_id": 325,
                        "po_id": 293,
                        "product": {
                            "pk": 645,
                            "name": "Tabl",
                            "category": "Sociis Natoque Company",
                            "quantity": 38276,
                            "identifier": "PROD17",
                            "location": "Schagen",
                            "description": "aldgjlakjlkasdj",
                            "prod_id": 645
                        },
                        "quantity": 250,
                        "receivedQty": 200,
                        "acceptedQty": 180,
                        "rejectedQty": 20,
                        "remark": "20 pieces faulty"
                    }
                ],
                "date": "29-Sep-2021",
                "vendor": {
                    "name": "Girish",
                    "identifier": "GJ",
                    "gstin": "GSTIN002",
                    "address": {
                        "name": "alsf",
                        "address": "jas;k",
                        "city": ";sdalkf",
                        "phone": "alsf",
                        "state": "kjdflk",
                        "country": "ljflkj",
                        "post": "54545"
                    }
                },
                "poRef": [
                    182
                ],
                "identifier": 846,
                "grnType": "auto",
                "amendDate": "2021-09-29T00:00:00Z",
                "transporter": "TeraTransport",
                "vehicleNumber": "GH-646358",
                "gateInwardNumber": "864353",
                "preparedBy": "KJL",
                "checkedBy": "KJH",
                "inspectedBy": "GIO",
                "approvedBy": "BHI"
            }
    
    """
    grnes = serializers.SerializerMethodField()
    date = serializers.DateTimeField(format="%d-%b-%Y")
    vendor = VendorSerializer()

    class Meta:
        model = GoodsReceiptNote
        fields = ('grnes','date','vendor','poRef','identifier','grnType','amendDate','transporter','vehicleNumber','gateInwardNumber','preparedBy','checkedBy','inspectedBy','approvedBy')

    def to_representation(self,instance):
        data = super().to_representation(instance)
        return data
    
    def get_grnes(self,instance):
        value = instance.grnentry_set
        if instance.grnType == 'auto':
            return GRNEntryWithPORefSerializer(value, many=True).data
        else:
            return GRNEntrySerializer(value, many=True).data
    
    # def create(self, validated_data):
    #     if self.data['grnType'] == 'auto':
    #         validated_data['grnes'] = GRNEntryWithPORefSerializer(source='grnentry_set', many=True)
    #     else:
    #         validated_data['grnes'] = GRNEntrySerializer(source='grnentry_set', many=True)
    #     prod = Product.objects.get(id=self.data['product']['prod_id'])
    #     return GoodsReceiptNote.objects.create(**validated_data)


class PSEntrySerializer(serializers.ModelSerializer):
    """Serializer for ``ProductSalesEntry`` class instance.

        The ``PSEntrySerializer.data`` attribute gives the ``JSON`` serialized data of the ``ProductSalesEntry`` instance::
        
            {
                "pse_id": 64,
                "product": {
                    "pk": 637,
                    "name": "Piano",
                    "category": "Ultricies PC",
                    "quantity": 23921,
                    "identifier": "PROD9",
                    "location": "Musselburgh",
                    "description": "88-key, Tri-sensor Scaled Hammer Action Keyboard II, Simulated ebony and ivory keys ",
                    "prod_id": 637
                },
                "quantity": 50,
                "price": 9900.0,
                "discount": 10.0,
                "order": 29
            }
    
    """
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
    """Serializer for ``SalesOrder`` class instance.

        The ``SalesOrderSerializer.data`` attribute gives the ``JSON`` serialized data of the ``SalesOrder`` instance::
        
            {
                "consumer": {
                    "name": "The Music Store",
                    "identifier": "CONS1256",
                    "gstin": "89AAC4633353643",
                    "phone": "+91 8325642358",
                    "address": "Plot no 958, N- 4, Neo Complex, Barh, Wokha, Nagaland, 797111",
                    "email": "JohnDoe@themusic.store",
                    "location": "Wokha"
                },
                "date": "2021-09-25T00:00:00Z",
                "so": 89,
                "subtotal": 744900.0,
                "taxtotal": 59592.0,
                "ordertotal": 804492.0,
                "pses": [
                    {
                        "pse_id": 64,
                        "product": {
                            "pk": 637,
                            "name": "piano",
                            "category": "Ultricies PC",
                            "quantity": 23921,
                            "identifier": "PROD9",
                            "location": "Musselburgh",
                            "description": "88-key, Tri-sensor Scaled Hammer Action Keyboard II, Simulated ebony and ivory keys ",
                            "prod_id": 637
                        },
                        "quantity": 50,
                        "price": 9900.0,
                        "discount": 10.0,
                        "order": 29
                    },
                    {
                        "pse_id": 65,
                        "product": {
                            "pk": 649,
                            "name": "Sabar",
                            "category": "Amet Consulting",
                            "quantity": 3903,
                            "identifier": "PROD21",
                            "location": "Serang",
                            "description": "High Sierra Sabar, Travel bag, Blue, Grey, Zipper, 36.5 L, 51.5 cm, 26 cm ",
                            "prod_id": 649
                        },
                        "quantity": 25,
                        "price": 4800.0,
                        "discount": 8.0,
                        "order": 29
                    },
                    {
                        "pse_id": 66,
                        "product": {
                            "pk": 654,
                            "name": "Parai",
                            "category": "Aliquet Lobortis Ltd",
                            "quantity": 8534,
                            "identifier": "PROD26",
                            "location": "Burhaniye",
                            "description": "Kannan musical instruments Parai 15" inch (Baffallow skin) Daf Instrument",
                            "prod_id": 654
                        },
                        "quantity": 35,
                        "price": 6000.0,
                        "discount": 10.0,
                        "order": 29
                    }
                ]
            }
    
    """
    consumer = ConsumerSerializer()
    pses = PSEntrySerializer(source='productsalesentry_set', many=True) 

    class Meta:
        model = SalesOrder
        fields = ('consumer','date','so','subtotal','taxtotal','ordertotal','pses')

    def to_representation(self,instance):
        data = super().to_representation(instance)
        return data   
    
    
class CompanySerializer(serializers.ModelSerializer):
    """Serializer for ``Company`` class instance.

        The ``CompanySerializer.data`` attribute gives the ``JSON`` serialized data of the ``Company`` instance::
        
            {
                "name": "Fringillami",
                "owner": "Ivor Barnett",
                "gstin": "89AAC056465468",
                "phone": "332 220-7026",
                "address": "Ap #849-6241 Euismod Av., 677598, Carinthia, Belgium",
                "email": "est.tempor@fringillami.org",
                "location": "Belgium",
                "image": "/media/images/logo.png"
            }
    
    """
    class Meta:
        model = Company
        fields = ('name','owner','gstin','phone','address','email','location','image')


class PurchaseInvoiceSerializer(serializers.ModelSerializer):
    """Serializer for ``PurchaseInvoice`` class instance.

        The ``PurchaseInvoiceSerializer.data`` attribute gives the ``JSON`` serialized data of the ``PurchaseInvoice`` instance::
        
            {
                "company": {
                    "name": "Fringillami",
                    "owner": "Ivor Barnett",
                    "gstin": "89AAC056465468",
                    "phone": "332 220-7026",
                    "address": "Ap #849-6241 Euismod Av., 677598, Carinthia, Belgium",
                    "email": "est.tempor@fringillami.org",
                    "location": "Belgium",
                    "image": "/media/images/logo.png"
                },
                "po": {
                    "vendor": {
                        "name": "Girish",
                        "identifier": "GJ",
                        "gstin": "GSTIN002",
                        "address": {
                            "name": "alsf",
                            "address": "jas;k",
                            "city": ";sdalkf",
                            "phone": "alsf",
                            "state": "kjdflk",
                            "country": "ljflkj",
                            "post": "54545"
                        }
                    },
                    "date": "25-Sep-2021",
                    "po": 293,
                    "subtotal": 279975.0,
                    "taxtotal": 22398.0,
                    "ordertotal": 302373.0,
                    "ppes": [
                        {
                            "ppe_id": 324,
                            "product": {
                                "pk": 637,
                                "name": "piano",
                                "category": "Ultricies PC",
                                "quantity": 23921,
                                "identifier": "PROD9",
                                "location": "Musselburgh",
                                "description": "88-key, Tri-sensor Scaled Hammer Action Keyboard II, Simulated ebony and ivory keys ",
                                "prod_id": 637
                            },
                            "quantity": 100,
                            "price": 10.0,
                            "discount": 0.0,
                            "order": 182,
                            "pendingQty": 50
                        },
                        {
                            "ppe_id": 325,
                            "product": {
                                "pk": 645,
                                "name": "Tabl",
                                "category": "Sociis Natoque Company",
                                "quantity": 38276,
                                "identifier": "PROD17",
                                "location": "Schagen",
                                "description": "aldgjlakjlkasdj",
                                "prod_id": 645
                            },
                            "quantity": 250,
                            "price": 90.0,
                            "discount": 8.0,
                            "order": 182,
                            "pendingQty": 70
                        },
                        {
                            "ppe_id": 326,
                            "product": {
                                "pk": 638,
                                "name": "Goblet drum",
                                "category": "Est Congue Consulting",
                                "quantity": 46076,
                                "identifier": "PROD10",
                                "location": "Kaluga",
                                "description": "aldgjlakjlkasdj",
                                "prod_id": 638
                            },
                            "quantity": 200,
                            "price": 150.0,
                            "discount": 12.0,
                            "order": 182,
                            "pendingQty": 200
                        },
                        {
                            "ppe_id": 327,
                            "product": {
                                "pk": 643,
                                "name": "quinto",
                                "category": "Enim Suspendisse Associates",
                                "quantity": 51099,
                                "identifier": "PROD15",
                                "location": "Nagpur",
                                "description": "aldgjlakjlkasdj",
                                "prod_id": 643
                            },
                            "quantity": 350,
                            "price": 150.0,
                            "discount": 10.0,
                            "order": 182,
                            "pendingQty": 350
                        },
                        {
                            "ppe_id": 328,
                            "product": {
                                "pk": 651,
                                "name": "Igihumurizo",
                                "category": "Curabitur Massa Vestibulum Consulting",
                                "quantity": 48553,
                                "identifier": "PROD23",
                                "location": "Yeovil",
                                "description": "aldgjlakjlkasdj",
                                "prod_id": 651
                            },
                            "quantity": 500,
                            "price": 50.0,
                            "discount": 6.0,
                            "order": 182,
                            "pendingQty": 500
                        },
                        {
                            "ppe_id": 329,
                            "product": {
                                "pk": 653,
                                "name": "Balsié",
                                "category": "Eu Foundation",
                                "quantity": 29988,
                                "identifier": "PROD25",
                                "location": "Sudbury",
                                "description": "aldgjlakjlkasdj",
                                "prod_id": 653
                            },
                            "quantity": 200,
                            "price": 500.0,
                            "discount": 15.0,
                            "order": 182,
                            "pendingQty": 200
                        },
                        {
                            "ppe_id": 330,
                            "product": {
                                "pk": 656,
                                "name": "Padayani thappu",
                                "category": "Posuere LLP",
                                "quantity": 6358,
                                "identifier": "PROD28",
                                "location": "Ruvo del Monte",
                                "description": "aldgjlakjlkasdj",
                                "prod_id": 656
                            },
                            "quantity": 350,
                            "price": 250.0,
                            "discount": 13.0,
                            "order": 182,
                            "pendingQty": 350
                        }
                    ]
                },
                "shippingaddress": {
                    "name": "Harding Gross",
                    "address": "8798 At, St., 7639",
                    "city": "Rome",
                    "phone": "936 651-4847",
                    "state": "Lazio",
                    "country": "Italy",
                    "post": "300326"
                },
                "communication": {
                    "email": "asfs@aflk.com",
                    "phone": "6546432"
                }
            }
    
    """
    company = CompanySerializer()
    po = PurchaseOrderSerializer()
    shippingaddress = ShippingAddressSerializer()
    communication = CommunicationSerializer()

    class Meta:
        model = PurchaseInvoice
        fields = ('company','po','shippingaddress','communication')
        
class GRNInvoiceSerializer(serializers.ModelSerializer):
    """Serializer for ``GRNInvoice`` class instance.

        The ``GRNInvoiceSerializer.data`` attribute gives the ``JSON`` serialized data of the ``GRNInvoice`` instance::
        
            {
                "company": {
                    "name": "Fringillami",
                    "owner": "Ivor Barnett",
                    "gstin": "89AAC056465468",
                    "phone": "332 220-7026",
                    "address": "Ap #849-6241 Euismod Av., 677598, Carinthia, Belgium",
                    "email": "est.tempor@fringillami.org",
                    "location": "Belgium",
                    "image": "/media/images/logo.png"
                },
                "grn": {
                    "grnes": [
                        {
                            "grn": 103,
                            "grne_id": 117,
                            "ppe_id": 324,
                            "po_id": 293,
                            "product": {
                                "pk": 637,
                                "name": "piano",
                                "category": "Ultricies PC",
                                "quantity": 23921,
                                "identifier": "PROD9",
                                "location": "Musselburgh",
                                "description": "88-key, Tri-sensor Scaled Hammer Action Keyboard II, Simulated ebony and ivory keys ",
                                "prod_id": 637
                            },
                            "quantity": 100,
                            "receivedQty": 50,
                            "acceptedQty": 50,
                            "rejectedQty": 0,
                            "remark": "OK"
                        },
                        {
                            "grn": 103,
                            "grne_id": 118,
                            "ppe_id": 325,
                            "po_id": 293,
                            "product": {
                                "pk": 645,
                                "name": "Tabl",
                                "category": "Sociis Natoque Company",
                                "quantity": 38276,
                                "identifier": "PROD17",
                                "location": "Schagen",
                                "description": "aldgjlakjlkasdj",
                                "prod_id": 645
                            },
                            "quantity": 250,
                            "receivedQty": 200,
                            "acceptedQty": 180,
                            "rejectedQty": 20,
                            "remark": "20 pieces faulty"
                        }
                    ],
                    "date": "29-Sep-2021",
                    "vendor": {
                        "name": "Girish",
                        "identifier": "GJ",
                        "gstin": "GSTIN002",
                        "address": {
                            "name": "alsf",
                            "address": "jas;k",
                            "city": ";sdalkf",
                            "phone": "alsf",
                            "state": "kjdflk",
                            "country": "ljflkj",
                            "post": "54545"
                        }
                    },
                    "poRef": [
                        182
                    ],
                    "identifier": 846,
                    "grnType": "auto",
                    "amendDate": "2021-09-29T00:00:00Z",
                    "transporter": "TeraTransport",
                    "vehicleNumber": "GH-646358",
                    "gateInwardNumber": "864353",
                    "preparedBy": "KJL",
                    "checkedBy": "KJH",
                    "inspectedBy": "GIO",
                    "approvedBy": "BHI"
                },
                "shippingaddress": {
                    "name": "Harding Gross",
                    "address": "8798 At, St., 7639",
                    "city": "Rome",
                    "phone": "936 651-4847",
                    "state": "Lazio",
                    "country": "Italy",
                    "post": "300326"
                },
                "communication": {
                    "email": "asfs@aflk.com",
                    "phone": "6546432"
                }
            }
    
    """
    company = CompanySerializer()
    grn = GoodsReceiptNoteSerializer()
    shippingaddress = ShippingAddressSerializer()
    communication = CommunicationSerializer()

    class Meta:
        model = PurchaseInvoice
        fields = ('company','grn','shippingaddress','communication')

class SalesInvoiceSerializer(serializers.ModelSerializer):
    """Serializer for ``SalesInvoice`` class instance.

        The ``SalesInvoiceSerializer.data`` attribute gives the ``JSON`` serialized data of the ``SalesInvoice`` instance::
        
            {
                "company": {
                    "name": "Fringillami",
                    "owner": "Ivor Barnett",
                    "gstin": "89AAC056465468",
                    "phone": "332 220-7026",
                    "address": "Ap #849-6241 Euismod Av., 677598, Carinthia, Belgium",
                    "email": "est.tempor@fringillami.org",
                    "location": "Belgium",
                    "image": "/media/images/hyperlink-green_x91WW5n.png"
                },
                "so": {
                    "consumer": {
                        "name": "The Music Store",
                        "identifier": "CONS1256",
                        "gstin": "89AAC4633353643",
                        "phone": "+91 8325642358",
                        "address": "Plot no 958, N- 4, Neo Complex, Barh, Wokha, Nagaland, 797111",
                        "email": "JohnDoe@themusic.store",
                        "location": "Wokha"
                    },
                    "date": "2021-09-25T00:00:00Z",
                    "so": 89,
                    "subtotal": 744900.0,
                    "taxtotal": 59592.0,
                    "ordertotal": 804492.0,
                    "pses": [
                        {
                            "pse_id": 64,
                            "product": {
                                "pk": 637,
                                "name": "piano",
                                "category": "Ultricies PC",
                                "quantity": 23921,
                                "identifier": "PROD9",
                                "location": "Musselburgh",
                                "description": "88-key, Tri-sensor Scaled Hammer Action Keyboard II, Simulated ebony and ivory keys ",
                                "prod_id": 637
                            },
                            "quantity": 50,
                            "price": 9900.0,
                            "discount": 10.0,
                            "order": 29
                        },
                        {
                            "pse_id": 65,
                            "product": {
                                "pk": 649,
                                "name": "Sabar",
                                "category": "Amet Consulting",
                                "quantity": 3903,
                                "identifier": "PROD21",
                                "location": "Serang",
                                "description": "High Sierra Sabar, Travel bag, Blue, Grey, Zipper, 36.5 L, 51.5 cm, 26 cm ",
                                "prod_id": 649
                            },
                            "quantity": 25,
                            "price": 4800.0,
                            "discount": 8.0,
                            "order": 29
                        },
                        {
                            "pse_id": 66,
                            "product": {
                                "pk": 654,
                                "name": "Parai",
                                "category": "Aliquet Lobortis Ltd",
                                "quantity": 8534,
                                "identifier": "PROD26",
                                "location": "Burhaniye",
                                "description": "Kannan musical instruments Parai 15" inch (Baffallow skin) Daf Instrument",
                                "prod_id": 654
                            },
                            "quantity": 35,
                            "price": 6000.0,
                            "discount": 10.0,
                            "order": 29
                        }
                    ]
                },
                "shippingaddress": {
                    "name": "Harding Gross",
                    "address": "8798 At, St., 7639",
                    "city": "Rome",
                    "phone": "936 651-4847",
                    "state": "Lazio",
                    "country": "Italy",
                    "post": "300326"
                }
            }
    
    """

    company = CompanySerializer()
    so = SalesOrderSerializer()
    shippingaddress = ShippingAddressSerializer()
    class Meta:
        model = SalesInvoice
        fields = ('company','so','shippingaddress')
        
        
class EventTypeSerializer(serializers.ModelSerializer):
    """Serializer for ``EventType`` class instance.

        The ``EventTypeSerializer.data`` attribute gives the ``JSON`` serialized data of the ``EventType`` instance::
        
            {
                "name": "# 85",
                "label": "Purchase Order"
            }
    
    """
    class Meta:
        model = EventType
        fields = ('created','updated','deleted')
        
        
class ObjectModelSerializer(serializers.ModelSerializer):
    """Serializer for ``ObjectModel`` class instance.

        The ``ObjectModelSerializer.data`` attribute gives the ``JSON`` serialized data of the ``ObjectModel`` instance::
        
            {
                "name": "# 85",
                "label": "Purchase Order",
                "modName": "PurchaseOrder"
            }
    
    """
    class Meta:
        model = ObjectModel
        fields = ('company', 'vendor','po', 'product', 'consumer', 'so')
    
    
class HistoryFilterStateSerializer(serializers.ModelSerializer):
    """Serializer for ``HistoryFilterState`` class instance.

        The ``HistoryFilterStateSerializer.data`` attribute gives the ``JSON`` serialized data of the ``HistoryFilterState`` instance::
        
            {
                "name": PreRelease20x,
                "numEntries" : 10,
                "eventTypes": {
                    "Created",
                    "Updated",
                    "Deleted"
                },
                "objModels": {
                    "Company",
                    "Vendor",
                    "PurchaseOrder",
                    "Product",
                    "Consumer",
                    "SalesOrder",
                    "GoodsReceiptNote"
                }
            }
    
    """
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