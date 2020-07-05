[33mcommit 3bacf1d15afc664757127f7f93c96c63bc6904ab[m[33m ([m[1;36mHEAD -> [m[1;32mmaster[m[33m, [m[1;31morigin/master[m[33m)[m
Author: Akisame Koetsuji <thephilosophicaljijutsumaster@gmail.com>
Date:   Mon May 4 23:13:45 2020 +0530

    Clean up.

[1mdiff --git a/pyVenv/src/InventoryManagement/InvManage/__pycache__/serializers.cpython-37.pyc b/pyVenv/src/InventoryManagement/InvManage/__pycache__/serializers.cpython-37.pyc[m
[1mindex 0b5e08a..b96c3a0 100644[m
Binary files a/pyVenv/src/InventoryManagement/InvManage/__pycache__/serializers.cpython-37.pyc and b/pyVenv/src/InventoryManagement/InvManage/__pycache__/serializers.cpython-37.pyc differ
[1mdiff --git a/pyVenv/src/InventoryManagement/InvManage/serializers.py b/pyVenv/src/InventoryManagement/InvManage/serializers.py[m
[1mindex 8593cea..cd6e2fa 100644[m
[1m--- a/pyVenv/src/InventoryManagement/InvManage/serializers.py[m
[1m+++ b/pyVenv/src/InventoryManagement/InvManage/serializers.py[m
[36m@@ -3,9 +3,10 @@[m [mfrom rest_framework import serializers[m
 from .models import Product, Vendor, ProductPurchaseEntry, PurchaseOrder, Company, Invoice, ShippingAddress[m
 [m
 class ProductSerializer(serializers.ModelSerializer):[m
[32m+[m[32m    prod_id = serializers.IntegerField(source='pk')[m
     class Meta:[m
         model = Product[m
[31m-        fields = ('pk','name','category','quantity','identifier','location','description')[m
[32m+[m[32m        fields = ('pk','name','category','quantity','identifier','location','description','prod_id')[m
 [m
     def to_representation(self, instance):[m
         data = super().to_representation(instance)[m
[36m@@ -21,7 +22,6 @@[m [mclass VendorSerializer(serializers.ModelSerializer):[m
         return data[m
 [m
 class PPEntrySerializer(serializers.ModelSerializer):[m
[31m-    # product = ProductSerializer()[m
     ppe_id = serializers.IntegerField(source='pk')[m
     product = ProductSerializer()[m
     class Meta:[m
[36m@@ -34,12 +34,17 @@[m [mclass PPEntrySerializer(serializers.ModelSerializer):[m
 [m
     def create(self, validated_data):[m
         validated_data.pop('pk')[m
[31m-        print(validated_data)[m
[32m+[m[32m        # print(self.data)[m
[32m+[m[32m        prod = Product.objects.get(id=self.data['product']['prod_id'])[m
[32m+[m[32m        validated_data['product']=prod[m
         return ProductPurchaseEntry.objects.create(**validated_data)[m
 [m
     def update(self, instance,validated_data):[m
[31m-        print(validated_data)[m
[31m-        instance.product = validated_data.get('product', instance.product)[m
[32m+[m[32m        # print(instance)[m
[32m+[m[32m        prod = Product.objects.get(id=validated_data['product']['pk'])[m
[32m+[m[32m        instance.product = prod[m
[32m+[m[32m        # print(validated_data)[m
[32m+[m[32m        # instance.product = validated_data.get('product', validated_data['product'])[m
         instance.quantity = validated_data.get('quantity', instance.quantity)[m
         instance.price = validated_data.get('price', instance.price)[m
         instance.discount = validated_data.get('discount', instance.discount)[m
[1mdiff --git a/pyVenv/src/InventoryManagement/InvManage/templates/purchase_order/po_products.html b/pyVenv/src/InventoryManagement/InvManage/templates/purchase_order/po_products.html[m
[1mindex c3af029..87eac9e 100644[m
[1m--- a/pyVenv/src/InventoryManagement/InvManage/templates/purchase_order/po_products.html[m
[1m+++ b/pyVenv/src/InventoryManagement/InvManage/templates/purchase_order/po_products.html[m
[36m@@ -26,7 +26,7 @@[m
           </div>[m
             <div>[m
               <table class="table" id="order_total">[m
[31m-                <form action=""></form>[m
[32m+[m[32m                <form action="">[m
                   <tbody id="order_total_body">[m
                     <tr>[m
                       <td>Subtotal</td>[m
[1mdiff --git a/pyVenv/src/InventoryManagement/InvManage/views/__pycache__/purchase_order_views.cpython-37.pyc b/pyVenv/src/InventoryManagement/InvManage/views/__pycache__/purchase_order_views.cpython-37.pyc[m
[1mindex ac5b5cc..a649316 100644[m
Binary files a/pyVenv/src/InventoryManagement/InvManage/views/__pycache__/purchase_order_views.cpython-37.pyc and b/pyVenv/src/InventoryManagement/InvManage/views/__pycache__/purchase_order_views.cpython-37.pyc differ
[1mdiff --git a/pyVenv/src/InventoryManagement/InvManage/views/purchase_order_views.py b/pyVenv/src/InventoryManagement/InvManage/views/purchase_order_views.py[m
[1mindex 7ae2cfa..7d50cb6 100644[m
[1m--- a/pyVenv/src/InventoryManagement/InvManage/views/purchase_order_views.py[m
[1m+++ b/pyVenv/src/InventoryManagement/InvManage/views/purchase_order_views.py[m
[36m@@ -5,266 +5,279 @@[m [mfrom django.forms.formsets import formset_factory[m
 from InvManage.models import *[m
 from InvManage.filters import PurchaseOrderFilter[m
 from django.http import JsonResponse[m
[31m-from InvManage.serializers import PPEntrySerializer, InvoiceSerializer[m
[32m+[m[32mfrom InvManage.serializers import ProductSerializer, PPEntrySerializer, InvoiceSerializer[m
 from InvManage.scripts.filters import *[m
 [m
[32m+[m
 def create_purchase_order_view(request):[m
[31m-	ProductPurchaseEntryFormset = formset_factory(ProductPurchaseEntryForm)[m
[31m-	data = {[m
[31m-		'form-TOTAL_FORMS': '0',[m
[31m-	    'form-INITIAL_FORMS': '0',[m
[31m-		'form-MAX_NUM_FORMS': '',[m
[31m-		}[m
[31m-	pentry_formset = ProductPurchaseEntryFormset(data)[m
[31m-	pentry_form = ProductPurchaseEntryForm()[m
[31m-	shipping_form = ShippingAddressForm()[m
[31m-	company = Company.objects.all().last()[m
[31m-	ship_data = company.shippingaddress.__dict__[m
[31m-	if request.method == 'GET':[m
[31m-		shipping_form = ShippingAddressForm(initial=ship_data)[m
[31m-		purchase_form = PurchaseOrderBasicInfo()[m
[31m-		vendor_form = VendorForm()[m
[31m-		prods = [][m
[31m-		for i,prod in enumerate(Product.objects.all()):[m
[31m-			prods.append({'id':prod.id,'name':prod.name,'code':prod.identifier})[m
[31m-		vendors = [][m
[31m-		for i,vend in enumerate(Vendor.objects.all()):[m
[31m-			vendors.append({'id': vend.id,'name':vend.name})[m
[31m-		context = {[m
[31m-			'purchase_form': purchase_form,[m
[31m-			'pentry_form': pentry_form,[m
[31m-			'prods': prods,[m
[31m-			'vendors': vendors,[m
[31m-			'vendor_form': vendor_form,[m
[31m-			'pentry_formset': pentry_formset,[m
[31m-			'ppes': {},[m
[31m-			'shipping_form': shipping_form,[m
[31m-			'requested_view_type':'create',[m
[31m-		}	[m
[31m-		return render(request, 'purchase_order.html',context)[m
[31m-	if request.method == 'POST':[m
[31m-		ProductPurchaseEntryFormset = formset_factory(ProductPurchaseEntryForm,can_delete=True)[m
[31m-		purchase_form = PurchaseOrderBasicInfo(request.POST, prefix='po')[m
[31m-		pentry_formset = ProductPurchaseEntryFormset(request.POST,prefix = 'form')[m
[31m-		data = {}[m
[31m-		print(purchase_form.is_valid())[m
[31m-		print(pentry_formset.is_valid())[m
[31m-		print(pentry_formset.errors)[m
[31m-		if purchase_form.is_valid():[m
[31m-			vendor = purchase_form.cleaned_data.get('vendor')[m
[31m-			po = purchase_form.cleaned_data.get('po')[m
[31m-			date = purchase_form.cleaned_data.get('date')[m
[31m-			tax = purchase_form.cleaned_data.get('tax')[m
[31m-			discount = purchase_form.cleaned_data.get('discount')[m
[31m-			paid = purchase_form.cleaned_data.get('paid')[m
[31m-			balance = purchase_form.cleaned_data.get('balance')[m
[31m-			subtotal = purchase_form.cleaned_data.get('subtotal')[m
[31m-			taxtotal = purchase_form.cleaned_data.get('taxtotal')[m
[31m-			ordertotal = purchase_form.cleaned_data.get('ordertotal')[m
[31m-			data = {[m
[31m-				'vendor':vendor,[m
[31m-				'po':po,[m
[31m-				'date':date,[m
[31m-				'tax':tax,[m
[31m-				'discount':discount,[m
[31m-				'paid':paid,[m
[31m-				'balance':balance,[m
[31m-				'subtotal':subtotal,[m
[31m-				'taxtotal':taxtotal,[m
[31m-				'ordertotal':ordertotal[m
[31m-			}[m
[31m-			new_po = PurchaseOrder.objects.create(**data)[m
[31m-			for ppeform in pentry_formset:[m
[31m-				if ppeform.is_valid():[m
[31m-					ppe_id = ppeform.cleaned_data.get('ppe_id')[m
[31m-					product = ppeform.cleaned_data.get('product')[m
[31m-					quantity = ppeform.cleaned_data.get('quantity')[m
[31m-					price = ppeform.cleaned_data.get('price')[m
[31m-					discount = ppeform.cleaned_data.get('discount')[m
[31m-					order = PurchaseOrder.objects.get(id=new_po.pk)[m
[31m-					print(ppe_id)[m
[31m-					validated_data = { 	'ppe_id': ppe_id,[m
[31m-										'product': product.pk,[m
[31m-										'quantity':quantity,[m
[31m-										'price':price,[m
[31m-										'discount':discount,[m
[31m-										'order':new_po.pk,[m
[31m-									}[m
[31m-					if ppe_id == -1: # new ppe to be created if id is -1[m
[31m-						pentry = PPEntrySerializer(data = validated_data)[m
[31m-						if pentry.is_valid():[m
[31m-							pentry.save()[m
[31m-							product.quantity += quantity # Add the quantity to the product stock as it is new ppe[m
[31m-						else:[m
[31m-							print(pentry.errors)[m
[31m-		return redirect('purchase_order')[m
[32m+[m[32m    ProductPurchaseEntryFormset = formset_factory(ProductPurchaseEntryForm)[m
[32m+[m[32m    data = {[m
[32m+[m[32m        'form-TOTAL_FORMS': '0',[m
[32m+[m[32m        'form-INITIAL_FORMS': '0',[m
[32m+[m[32m        'form-MAX_NUM_FORMS': '',[m
[32m+[m[32m    }[m
[32m+[m[32m    pentry_formset = ProductPurchaseEntryFormset(data)[m
[32m+[m[32m    pentry_form = ProductPurchaseEntryForm()[m
[32m+[m[32m    shipping_form = ShippingAddressForm()[m
[32m+[m[32m    company = Company.objects.all().last()[m
[32m+[m[32m    ship_data = company.shippingaddress.__dict__[m
[32m+[m[32m    if request.method == 'GET':[m
[32m+[m[32m        shipping_form = ShippingAddressForm(initial=ship_data)[m
[32m+[m[32m        purchase_form = PurchaseOrderBasicInfo()[m
[32m+[m[32m        vendor_form = VendorForm()[m
[32m+[m[32m        prods = [][m
[32m+[m[32m        for i, prod in enumerate(Product.objects.all()):[m
[32m+[m[32m            prods.append({'id': prod.id, 'name': prod.name,[m
[32m+[m[32m                          'code': prod.identifier})[m
[32m+[m[32m        vendors = [][m
[32m+[m[32m        for i, vend in enumerate(Vendor.objects.all()):[m
[32m+[m[32m            vendors.append({'id': vend.id, 'name': vend.name})[m
[32m+[m[32m        context = {[m
[32m+[m[32m            'purchase_form': purchase_form,[m
[32m+[m[32m            'pentry_form': pentry_form,[m
[32m+[m[32m            'prods': prods,[m
[32m+[m[32m            'vendors': vendors,[m
[32m+[m[32m            'vendor_form': vendor_form,[m
[32m+[m[32m            'pentry_formset': pentry_formset,[m
[32m+[m[32m            'ppes': {},[m
[32m+[m[32m            'shipping_form': shipping_form,[m
[32m+[m[32m            'requested_view_type': 'create',[m
[32m+[m[32m        }[m
[32m+[m[32m        return render(request, 'purchase_order.html', context)[m
[32m+[m[32m    if request.method == 'POST':[m
[32m+[m[32m        ProductPurchaseEntryFormset = formset_factory([m
[32m+[m[32m            ProductPurchaseEntryForm, can_delete=True)[m
[32m+[m[32m        purchase_form = PurchaseOrderBasicInfo(request.POST, prefix='po')[m
[32m+[m[32m        pentry_formset = ProductPurchaseEntryFormset([m
[32m+[m[32m            request.POST, prefix='form')[m
[32m+[m[32m        data = {}[m
[32m+[m[32m        print(purchase_form.is_valid())[m
[32m+[m[32m        print(pentry_formset.is_valid())[m
[32m+[m[32m        print(pentry_formset.errors)[m
[32m+[m[32m        if purchase_form.is_valid():[m
[32m+[m[32m            vendor = purchase_form.cleaned_data.get('vendor')[m
[32m+[m[32m            po = purchase_form.cleaned_data.get('po')[m
[32m+[m[32m            date = purchase_form.cleaned_data.get('date')[m
[32m+[m[32m            tax = purchase_form.cleaned_data.get('tax')[m
[32m+[m[32m            discount = purchase_form.cleaned_data.get('discount')[m
[32m+[m[32m            paid = purchase_form.cleaned_data.get('paid')[m
[32m+[m[32m            balance = purchase_form.cleaned_data.get('balance')[m
[32m+[m[32m            subtotal = purchase_form.cleaned_data.get('subtotal')[m
[32m+[m[32m            taxtotal = purchase_form.cleaned_data.get('taxtotal')[m
[32m+[m[32m            ordertotal = purchase_form.cleaned_data.get('ordertotal')[m
[32m+[m[32m            data = {[m
[32m+[m[32m                'vendor': vendor,[m
[32m+[m[32m                'po': po,[m
[32m+[m[32m                'date': date,[m
[32m+[m[32m                'tax': tax,[m
[32m+[m[32m                'discount': discount,[m
[32m+[m[32m                'paid': paid,[m
[32m+[m[32m                'balance': balance,[m
[32m+[m[32m                'subtotal': subtotal,[m
[32m+[m[32m                'taxtotal': taxtotal,[m
[32m+[m[32m                'ordertotal': ordertotal[m
[32m+[m[32m            }[m
[32m+[m[32m            new_po = PurchaseOrder.objects.create(**data)[m
[32m+[m[32m            for ppeform in pentry_formset:[m
[32m+[m[32m                if ppeform.is_valid():[m
[32m+[m[32m                    ppe_id = ppeform.cleaned_data.get('ppe_id')[m
[32m+[m[32m                    product = ppeform.cleaned_data.get('product')[m
[32m+[m[32m                    quantity = ppeform.cleaned_data.get('quantity')[m
[32m+[m[32m                    price = ppeform.cleaned_data.get('price')[m
[32m+[m[32m                    discount = ppeform.cleaned_data.get('discount')[m
[32m+[m[32m                    order = PurchaseOrder.objects.get(id=new_po.pk)[m
[32m+[m[32m                    print(ppe_id)[m
[32m+[m[32m                    validated_data = {'ppe_id': ppe_id,[m
[32m+[m[32m                                      'product': product.pk,[m
[32m+[m[32m                                      'quantity': quantity,[m
[32m+[m[32m                                      'price': price,[m
[32m+[m[32m                                      'discount': discount,[m
[32m+[m[32m                                      'order': new_po.pk,[m
[32m+[m[32m                                      }[m
[32m+[m[32m                    if ppe_id == -1:  # new ppe to be created if id is -1[m
[32m+[m[32m                        pentry = PPEntrySerializer(data=validated_data)[m
[32m+[m[32m                        if pentry.is_valid():[m
[32m+[m[32m                            pentry.save()[m
[32m+[m[32m                            product.quantity += quantity  # Add the quantity to the product stock as it is new ppe[m
[32m+[m[32m                        else:[m
[32m+[m[32m                            print(pentry.errors)[m
[32m+[m[32m        return redirect('purchase_order')[m
[32m+[m
 [m
 def display_purchase_orders_view(request):[m
[31m-	if request.method == 'GET':[m
[31m-		pos = sort_ascending_descending(request,PurchaseOrder)[m
[31m-		state = FilterState.objects.get(name='POs_basic')[m
[31m-		column_list = change_column_position(request, state)[m
[31m-		myFilter = PurchaseOrderFilter(request.GET, queryset=pos)[m
[31m-		queryset = myFilter.qs[m
[31m-		number_of_objects = len(queryset)[m
[31m-		page_number = request.GET.get('page')[m
[31m-		print(number_of_objects)[m
[31m-		page_obj, dictionaries = paginate(queryset,myFilter,page_number)[m
[31m-		print(page_obj)[m
[31m-		for dict in dictionaries: # dictionary contains only vendor id and not vendor name. So add it.[m
[31m-			vend_id = dict['vendor_id'][m
[31m-			vendor = Vendor.objects.get(id=vend_id)[m
[31m-			dict['vendor'] = vendor.name[m
[31m-		print(dictionaries)[m
[31m-		print(column_list)[m
[31m-		return render(request, 'purchase_order/purchase_order_contents.html',{'page_obj':page_obj,[m
[31m-															'myFilter':myFilter,[m
[31m-															'n_prod': number_of_objects,[m
[31m-															'columns': column_list,[m
[31m-															'dicts': dictionaries})[m
[32m+[m[32m    if request.method == 'GET':[m
[32m+[m[32m        pos = sort_ascending_descending(request, PurchaseOrder)[m
[32m+[m[32m        state = FilterState.objects.get(name='POs_basic')[m
[32m+[m[32m        column_list = change_column_position(request, state)[m
[32m+[m[32m        myFilter = PurchaseOrderFilter(request.GET, queryset=pos)[m
[32m+[m[32m        queryset = myFilter.qs[m
[32m+[m[32m        number_of_objects = len(queryset)[m
[32m+[m[32m        page_number = request.GET.get('page')[m
[32m+[m[32m        page_obj, dictionaries = paginate(queryset, myFilter, page_number)[m
[32m+[m[32m        # dictionary contains only vendor id and not vendor name. So add it.[m
[32m+[m[32m        for dict in dictionaries:[m
[32m+[m[32m            vend_id = dict['vendor_id'][m
[32m+[m[32m            vendor = Vendor.objects.get(id=vend_id)[m
[32m+[m[32m            dict['vendor'] = vendor.name[m
[32m+[m[32m        return render(request, 'purchase_order/purchase_order_contents.html', {'page_obj': page_obj,[m
[32m+[m[32m                                                                               'myFilter': myFilter,[m
[32m+[m[32m                                                                               'n_prod': number_of_objects,[m
[32m+[m[32m                                                                               'columns': column_list,[m
[32m+[m[32m                                                                               'dicts': dictionaries})[m
[32m+[m
[32m+[m
[32m+[m[32mdef delete_purchase_order_view(request, pk):[m
[32m+[m[32m    if request.method == 'POST':[m
[32m+[m[32m        po = PurchaseOrder.objects.get(id=pk)[m
[32m+[m[32m        po.delete()[m
[32m+[m[32m        return redirect('purchase_order')[m
 [m
[31m-def delete_purchase_order_view(request,pk):[m
[31m-	if request.method == 'POST':[m
[31m-		po = PurchaseOrder.objects.get(id=pk)[m
[31m-		po.delete()[m
[31m-		return redirect('purchase_order')[m
 [m
 def update_purchase_order_view(request):[m
[31m-	if request.method == 'GET':[m
[31m-		pk = request.GET.get('pk')[m
[31m-		print(pk)[m
[31m-		po = PurchaseOrder.objects.get(id=pk)[m
[31m-		po_data = po.__dict__[m
[31m-		vendor = po.vendor[m
[31m-		ven_data = vendor.__dict__[m
[31m-		company = Company.objects.all().last()[m
[31m-		ship_data = company.shippingaddress.__dict__[m
[31m-		ProductPurchaseEntryFormset = formset_factory(ProductPurchaseEntryForm,can_delete=True)[m
[31m-		ppes = PurchaseOrder.objects.get(id=pk).productpurchaseentry_set.all()[m
[31m-		ppes_serialized = [][m
[31m-		for ppe in ppes:[m
[31m-			d = PPEntrySerializer(ppe)[m
[31m-			ppes_serialized.append(d.data)[m
[31m-		data = {[m
[31m-			'form-TOTAL_FORMS': len(ppes),[m
[31m-			'form-INITIAL_FORMS': len(ppes),[m
[31m-			'form-MAX_NUM_FORMS': '',[m
[31m-		}[m
[31m-		pentry_formset = ProductPurchaseEntryFormset(data,initial=ppes)[m
[31m-		pentry_form = ProductPurchaseEntryForm()[m
[31m-		purchase_form = PurchaseOrderBasicInfo(initial=po_data)[m
[31m-		print(purchase_form)[m
[31m-		vendor_form = VendorForm(initial=ven_data)[m
[31m-		shipping_form = ShippingAddressForm(initial=ship_data)[m
[31m-		prods = [][m
[31m-		for i,prod in enumerate(Product.objects.all()):[m
[31m-			prods.append({'id':prod.id,'name':prod.name,'code':prod.identifier})[m
[31m-		vendors = [][m
[31m-		for i,vend in enumerate(Vendor.objects.all()):[m
[31m-			vendors.append({'id': vend.id,'name':vend.name})[m
[31m-		context = {[m
[31m-			'purchase_form': purchase_form,[m
[31m-			'pentry_form': pentry_form,[m
[31m-			'prods': prods,[m
[31m-			'vendor_id': vendor.pk,[m
[31m-			'vendors': vendors,[m
[31m-			'vendor_form': vendor_form,[m
[31m-			'pentry_formset': pentry_formset,[m
[31m-			'ppes': ppes_serialized,[m
[31m-			'shipping_form':shipping_form,[m
[31m-			'requested_view_type':'update',[m
[31m-			'pk':pk,[m
[31m-		}	[m
[31m-		return render(request, 'purchase_order/update_purchase_order.html',context)[m
[31m-	if request.method == 'POST':[m
[31m-		pk = request.POST.get('pk')[m
[31m-		print(pk)[m
[31m-		ProductPurchaseEntryFormset = formset_factory(ProductPurchaseEntryForm,can_delete=True)[m
[31m-		purchase_form = PurchaseOrderBasicInfo(request.POST, prefix='po')[m
[31m-		pentry_formset = ProductPurchaseEntryFormset(request.POST,prefix = 'form')[m
[31m-		data = {}[m
[31m-		print(purchase_form.is_valid())[m
[31m-		print(pentry_formset.is_valid())[m
[31m-		if purchase_form.is_valid():[m
[31m-			vendor = purchase_form.cleaned_data.get('vendor')[m
[31m-			po = purchase_form.cleaned_data.get('po')[m
[31m-			date = purchase_form.cleaned_data.get('date')[m
[31m-			tax = purchase_form.cleaned_data.get('tax')[m
[31m-			discount = purchase_form.cleaned_data.get('discount')[m
[31m-			paid = purchase_form.cleaned_data.get('paid')[m
[31m-			balance = purchase_form.cleaned_data.get('balance')[m
[31m-			subtotal = purchase_form.cleaned_data.get('subtotal')[m
[31m-			taxtotal = purchase_form.cleaned_data.get('taxtotal')[m
[31m-			ordertotal = purchase_form.cleaned_data.get('ordertotal')[m
[31m-			data = {[m
[31m-				'vendor':vendor,[m
[31m-				'po':po,[m
[31m-				'date':date,[m
[31m-				'tax':tax,[m
[31m-				'discount':discount,[m
[31m-				'paid':paid,[m
[31m-				'balance':balance,[m
[31m-				'subtotal':subtotal,[m
[31m-				'taxtotal':taxtotal,[m
[31m-				'ordertotal':ordertotal[m
[31m-			}[m
[31m-			PurchaseOrder.objects.filter(id=pk).update(**data)[m
[31m-			for ppeform in pentry_formset:[m
[31m-				if ppeform.is_valid():[m
[31m-					ppe_id = ppeform.cleaned_data.get('ppe_id')[m
[31m-					product = ppeform.cleaned_data.get('product')[m
[31m-					quantity = ppeform.cleaned_data.get('quantity')[m
[31m-					price = ppeform.cleaned_data.get('price')[m
[31m-					discount = ppeform.cleaned_data.get('discount')[m
[31m-					order = PurchaseOrder.objects.get(id=pk)[m
[31m-					print(ppe_id)[m
[31m-					validated_data = { 	'ppe_id': ppe_id,[m
[31m-										'product': product.pk,[m
[31m-										'quantity':quantity,[m
[31m-										'price':price,[m
[31m-										'discount':discount,[m
[31m-										'order':pk,[m
[31m-									}[m
[31m-					if ppe_id == -1: # new ppe to be created if id is -1[m
[31m-						pentry = PPEntrySerializer(data = validated_data)[m
[31m-						if pentry.is_valid():[m
[31m-							pentry.save()[m
[31m-							product.quantity += quantity # Add the quantity to the product stock as it is new ppe[m
[31m-						else:[m
[31m-							print(pentry.errors)[m
[31m-					else:[m
[31m-						ppe=ProductPurchaseEntry.objects.get(id=ppe_id)[m
[31m-						print(ppe)[m
[31m-						old_quantity = ppe.quantity[m
[31m-						# ppeform.cleaned_data.update({'order':order})[m
[31m-						# validated_data.update({'ppe_id': ppe_id})[m
[31m-						print(validated_data)[m
[31m-						pentry = PPEntrySerializer(ppe,data = validated_data)[m
[31m-						if pentry.is_valid():[m
[31m-							pentry.save()[m
[31m-							# ProductPurchaseEntry.objects.filter(id=ppe_id).update(product=product,quantity=quantity,price=price,discount=discount,order=order)[m
[31m-							product.quantity += quantity-old_quantity # Add the difference of quantity to the product stock as it is updated ppe[m
[31m-							product.save() # Save the changes to the product instance[m
[31m-						else:[m
[31m-							print(pentry.errors)[m
[31m-			for ppeform in pentry_formset.deleted_forms:[m
[31m-				print(ppeform.is_valid())[m
[31m-				ppe_id = ppeform.cleaned_data.get('ppe_id')[m
[31m-				print(ppe_id)[m
[31m-				product = ppeform.cleaned_data.get('product')[m
[31m-				quantity = ppeform.cleaned_data.get('quantity')[m
[31m-				if ppe_id != -1:[m
[31m-					ppe = ProductPurchaseEntry.objects.get(id=ppe_id)[m
[31m-					product.quantity -= quantity[m
[31m-					ppe.delete()[m
[31m-		return redirect('purchase_order')[m
[32m+[m[32m    if request.method == 'GET':[m
[32m+[m[32m        pk = request.GET.get('pk')[m
[32m+[m[32m        print(pk)[m
[32m+[m[32m        po = PurchaseOrder.objects.get(id=pk)[m
[32m+[m[32m        po_data = po.__dict__[m
[32m+[m[32m        vendor = po.vendor[m
[32m+[m[32m        ven_data = vendor.__dict__[m
[32m+[m[32m        company = Company.objects.all().last()[m
[32m+[m[32m        ship_data = company.shippingaddress.__dict__[m
[32m+[m[32m        ProductPurchaseEntryFormset = formset_factory([m
[32m+[m[32m            ProductPurchaseEntryForm, can_delete=True)[m
[32m+[m[32m        ppes = PurchaseOrder.objects.get(id=pk).productpurchaseentry_set.all()[m
[32m+[m[32m        ppes_serialized = [][m
[32m+[m[32m        for ppe in ppes:[m
[32m+[m[32m            d = PPEntrySerializer(ppe)[m
[32m+[m[32m            ppes_serialized.append(d.data)[m
[32m+[m[32m        data = {[m
[32m+[m[32m            'form-TOTAL_FORMS': len(ppes),[m
[32m+[m[32m            'form-INITIAL_FORMS': len(ppes),[m
[32m+[m[32m            'form-MAX_NUM_FORMS': '',[m
[32m+[m[32m        }[m
[32m+[m[32m        pentry_formset = ProductPurchaseEntryFormset(data, initial=ppes)[m
[32m+[m[32m        pentry_form = ProductPurchaseEntryForm()[m
[32m+[m[32m        purchase_form = PurchaseOrderBasicInfo(initial=po_data)[m
[32m+[m[32m        # print(purchase_form)[m
[32m+[m[32m        vendor_form = VendorForm(initial=ven_data)[m
[32m+[m[32m        shipping_form = ShippingAddressForm(initial=ship_data)[m
[32m+[m[32m        prods = [][m
[32m+[m[32m        for i, prod in enumerate(Product.objects.all()):[m
[32m+[m[32m            prods.append({'id': prod.id, 'name': prod.name,[m
[32m+[m[32m                          'code': prod.identifier})[m
[32m+[m[32m        vendors = [][m
[32m+[m[32m        for i, vend in enumerate(Vendor.objects.all()):[m
[32m+[m[32m            vendors.append({'id': vend.id, 'name': vend.name})[m
[32m+[m[32m        context = {[m
[32m+[m[32m            'purchase_form': purchase_form,[m
[32m+[m[32m            'pentry_form': pentry_form,[m
[32m+[m[32m            'prods': prods,[m
[32m+[m[32m            'vendor_id': vendor.pk,[m
[32m+[m[32m            'vendors': vendors,[m
[32m+[m[32m            'vendor_form': vendor_form,[m
[32m+[m[32m            'pentry_formset': pentry_formset,[m
[32m+[m[32m            'ppes': ppes_serialized,[m
[32m+[m[32m            'shipping_form': shipping_form,[m
[32m+[m[32m            'requested_view_type': 'update',[m
[32m+[m[32m            'pk': pk,[m
[32m+[m[32m        }[m
[32m+[m[32m        return render(request, 'purchase_order/update_purchase_order.html', context)[m
[32m+[m[32m    if request.method == 'POST':[m
[32m+[m[32m        pk = request.POST.get('pk')[m
[32m+[m[32m        print(pk)[m
[32m+[m[32m        ProductPurchaseEntryFormset = formset_factory([m
[32m+[m[32m            ProductPurchaseEntryForm, can_delete=True)[m
[32m+[m[32m        purchase_form = PurchaseOrderBasicInfo(request.POST, prefix='po')[m
[32m+[m[32m        pentry_formset = ProductPurchaseEntryFormset([m
[32m+[m[32m            request.POST, prefix='form')[m
[32m+[m[32m        data = {}[m
[32m+[m[32m        print(purchase_form.is_valid())[m
[32m+[m[32m        print(pentry_formset.is_valid())[m
[32m+[m[32m        if purchase_form.is_valid():[m
[32m+[m[32m            vendor = purchase_form.cleaned_data.get('vendor')[m
[32m+[m[32m            po = purchase_form.cleaned_data.get('po')[m
[32m+[m[32m            date = purchase_form.cleaned_data.get('date')[m
[32m+[m[32m            tax = purchase_form.cleaned_data.get('tax')[m
[32m+[m[32m            discount = purchase_form.cleaned_data.get('discount')[m
[32m+[m[32m            paid = purchase_form.cleaned_data.get('paid')[m
[32m+[m[32m            balance = purchase_form.cleaned_data.get('balance')[m
[32m+[m[32m            subtotal = purchase_form.cleaned_data.get('subtotal')[m
[32m+[m[32m            taxtotal = purchase_form.cleaned_data.get('taxtotal')[m
[32m+[m[32m            ordertotal = purchase_form.cleaned_data.get('ordertotal')[m
[32m+[m[32m            data = {[m
[32m+[m[32m                'vendor': vendor,[m
[32m+[m[32m                'po': po,[m
[32m+[m[32m                'date': date,[m
[32m+[m[32m                'tax': tax,[m
[32m+[m[32m                'discount': discount,[m
[32m+[m[32m                'paid': paid,[m
[32m+[m[32m                'balance': balance,[m
[32m+[m[32m                'subtotal': subtotal,[m
[32m+[m[32m                'taxtotal': taxtotal,[m
[32m+[m[32m                'ordertotal': ordertotal[m
[32m+[m[32m            }[m
[32m+[m[32m            PurchaseOrder.objects.filter(id=pk).update(**data)[m
[32m+[m[32m            for ppeform in pentry_formset:[m
[32m+[m[32m                if ppeform.is_valid():[m
[32m+[m[32m                    ppe_id = ppeform.cleaned_data.get('ppe_id')[m
[32m+[m[32m                    product = ppeform.cleaned_data.get('product')[m
[32m+[m[32m                    quantity = ppeform.cleaned_data.get('quantity')[m
[32m+[m[32m                    price = ppeform.cleaned_data.get('price')[m
[32m+[m[32m                    discount = ppeform.cleaned_data.get('discount')[m
[32m+[m[32m                    order = PurchaseOrder.objects.get(id=pk)[m
[32m+[m[32m                    print(ppe_id)[m
[32m+[m[32m                    validated_data = {'ppe_id': ppe_id,[m
[32m+[m[32m                                    #   'product': product.__dict__,[m
[32m+[m[32m                                      'product': ProductSerializer(product).data,[m
[32m+[m[32m                                      'quantity': quantity,[m
[32m+[m[32m                                      'price': price,[m
[32m+[m[32m                                      'discount': discount,[m
[32m+[m[32m                                      'order': pk,[m
[32m+[m[32m                                      }[m
[32m+[m[32m                    if ppe_id == -1:  # new ppe to be created if id is -1[m
[32m+[m[32m                        pentry = PPEntrySerializer(data=validated_data)[m
[32m+[m[32m                        if pentry.is_valid():[m
[32m+[m[32m                            pentry.save()[m
[32m+[m[32m                            product.quantity += quantity  # Add the quantity to the product stock as it is new ppe[m
[32m+[m[32m                        else:[m
[32m+[m[32m                            print(pentry.errors)[m
[32m+[m[32m                    else:[m
[32m+[m[32m                        ppe = ProductPurchaseEntry.objects.get(id=ppe_id)[m
[32m+[m[32m                        # print(ppe)[m
[32m+[m[32m                        old_quantity = ppe.quantity[m
[32m+[m[32m                        # ppeform.cleaned_data.update({'order':order})[m
[32m+[m[32m                        # validated_data.update({'ppe_id': ppe_id})[m
[32m+[m[32m                        # print(validated_data)[m
[32m+[m[32m                        pentry = PPEntrySerializer(ppe, data=validated_data)[m
[32m+[m[32m                        if pentry.is_valid():[m
[32m+[m[32m                            # print(validated_data)[m
[32m+[m[32m                            pentry.save()[m
[32m+[m[32m                            # ProductPurchaseEntry.objects.filter(id=ppe_id).update(product=product,quantity=quantity,price=price,discount=discount,order=order)[m
[32m+[m[32m                            # Add the difference of quantity to the product stock as it is updated ppe[m
[32m+[m[32m                            product.quantity += quantity-old_quantity[m
[32m+[m[32m                            product.save()  # Save the changes to the product instance[m
[32m+[m[32m                        else:[m
[32m+[m[32m                            print(pentry.errors)[m
[32m+[m[32m            for ppeform in pentry_formset.deleted_forms:[m
[32m+[m[32m                print(ppeform.is_valid())[m
[32m+[m[32m                ppe_id = ppeform.cleaned_data.get('ppe_id')[m
[32m+[m[32m                print(ppe_id)[m
[32m+[m[32m                product = ppeform.cleaned_data.get('product')[m
[32m+[m[32m                quantity = ppeform.cleaned_data.get('quantity')[m
[32m+[m[32m                if ppe_id != -1:[m
[32m+[m[32m                    ppe = ProductPurchaseEntry.objects.get(id=ppe_id)[m
[32m+[m[32m                    product.quantity -= quantity[m
[32m+[m[32m                    ppe.delete()[m
[32m+[m[32m        return redirect('purchase_order')[m
[32m+[m
 [m
[31m-def print_purchase_order_view(request,pk):[m
[31m-	if request.method == 'GET':[m
[31m-		po = PurchaseOrder.objects.get(id=pk)[m
[31m-		company = Company.objects.all().last()[m
[31m-		shippingaddress = company.shippingaddress[m
[31m-		print(shippingaddress)[m
[31m-		invoice_serializer = InvoiceSerializer(Invoice(company=company,po=po,shippingaddress=shippingaddress))[m
[31m-		print(invoice_serializer.data)[m
[31m-	return JsonResponse(invoice_serializer.data)[m
[32m+[m[32mdef print_purchase_order_view(request, pk):[m
[32m+[m[32m    if request.method == 'GET':[m
[32m+[m[32m        po = PurchaseOrder.objects.get(id=pk)[m
[32m+[m[32m        company = Company.objects.all().last()[m
[32m+[m[32m        shippingaddress = company.shippingaddress[m
[32m+[m[32m        print(shippingaddress)[m
[32m+[m[32m        invoice_serializer = InvoiceSerializer([m
[32m+[m[32m            Invoice(company=company, po=po, shippingaddress=shippingaddress))[m
[32m+[m[32m        print(invoice_serializer.data)[m
[32m+[m[32m    return JsonResponse(invoice_serializer.data)[m
[1mdiff --git a/pyVenv/src/InventoryManagement/InventoryManagement/media/logo_DyCPZVB.png b/pyVenv/src/InventoryManagement/InventoryManagement/media/logo_DyCPZVB.png[m
[1mnew file mode 100644[m
[1mindex 0000000..e6dc53f[m
Binary files /dev/null and b/pyVenv/src/InventoryManagement/InventoryManagement/media/logo_DyCPZVB.png differ
[1mdiff --git a/pyVenv/src/InventoryManagement/db.sqlite3 b/pyVenv/src/InventoryManagement/db.sqlite3[m
[1mindex 377c635..67c86f9 100644[m
Binary files a/pyVenv/src/InventoryManagement/db.sqlite3 and b/pyVenv/src/InventoryManagement/db.sqlite3 differ
