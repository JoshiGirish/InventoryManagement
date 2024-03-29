import django_filters
from .models import *
from django_filters import CharFilter
from django import forms

class ProductFilter(django_filters.FilterSet):
    context = {'class':'form-control form-control-sm','onchange':'fetchData(this);enableHighlight();'}
    name = django_filters.CharFilter(field_name='name', lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    category = django_filters.CharFilter(field_name='category',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    quantity = django_filters.CharFilter(field_name='quantity',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    price = django_filters.CharFilter(field_name='price',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    identifier = django_filters.CharFilter(field_name='identifier',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    location = django_filters.CharFilter(field_name='location',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    order_by_field = 'ordering'
    ordering = django_filters.OrderingFilter(
        fields = (
            ('name','name'),
            ('category','category'),
            ('quantity', 'quantity'),
            ('price','price'),
            ('identifier','identifier'),
            ('location', 'location')
        )
    )
    class Meta:
        model = Product
        fields = {}

class VendorFilter(django_filters.FilterSet):
    context = {'class':'form-control form-control-sm','onchange':'fetchData(this);enableHighlight();'}
    name = django_filters.CharFilter(field_name='name', lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    identifier = django_filters.CharFilter(field_name='identifier',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    phone = django_filters.CharFilter(field_name='address__phone',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    email = django_filters.CharFilter(field_name='communication__email',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    location = django_filters.CharFilter(field_name='address__city',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    order_by_field = 'ordering'
    ordering = django_filters.OrderingFilter(
        fields = (
            ('name','name'),
            ('identifier','identifier'),
            ('address__phone', 'phone'),
            ('communication__email', 'email'),
            ('address__city', 'location')
        )
    )
    class Meta:
        model = Vendor
        fields = {'name','identifier', 'phone', 'email', 'location'}
        
        
class ConsumerFilter(django_filters.FilterSet):
    context = {'class':'form-control form-control-sm','onchange':'fetchData(this);enableHighlight();'}
    name = django_filters.CharFilter(field_name='name', lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    identifier = django_filters.CharFilter(field_name='identifier',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    phone = django_filters.CharFilter(field_name='phone',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    email = django_filters.CharFilter(field_name='email',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    location = django_filters.CharFilter(field_name='location',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    order_by_field = 'ordering'
    ordering = django_filters.OrderingFilter(
        fields = (
            ('name','name'),
            ('identifier', 'identifier'),
            ('phone','phone'),
            ('email', 'email'),
            ('location','location')
        )
    )
    class Meta:
        model = Consumer
        fields = {}

class PurchaseOrderFilter(django_filters.FilterSet):
    context = {'class':'form-control form-control-sm','onchange':'fetchData(this);enableHighlight();'}
    vendor = django_filters.CharFilter(field_name='vendor__name', lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    date = django_filters.CharFilter(field_name='date',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    po = django_filters.CharFilter(field_name='po',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    ordertotal = django_filters.CharFilter(field_name='ordertotal',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    order_by_field = 'ordering'
    ordering = django_filters.OrderingFilter(
        fields = (
            ('vendor__name','vendor'),
            ('date','date'),
            ('po', 'po'),
            ('ordertotal', 'ordertotal'),
        )
    )
    class Meta:
        model = PurchaseOrder
        fields = {}
        
        
class GoodsReceiptNoteFilter(django_filters.FilterSet):
    context = {'class':'form-control form-control-sm','onchange':'fetchData(this);enableHighlight();'}
    identifier = django_filters.CharFilter(field_name='identifier',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    vendor = django_filters.CharFilter(field_name='vendor__name', lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    date = django_filters.CharFilter(field_name='date',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    poRef = django_filters.CharFilter(field_name='poRef',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    grnType = django_filters.CharFilter(field_name='grnType',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    amendNumber = django_filters.CharFilter(field_name='amendNumber',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    amendDate = django_filters.CharFilter(field_name='amendDate',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    vehicleNumber = django_filters.CharFilter(field_name='vehicleNumber',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    gateInwardNumber = django_filters.CharFilter(field_name='gateInwardNumber',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    preparedBy = django_filters.CharFilter(field_name='preparedBy',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    checkedBy = django_filters.CharFilter(field_name='checkedBy',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    inspectedBy = django_filters.CharFilter(field_name='inspectedBy',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    approvedBy = django_filters.CharFilter(field_name='approvedBy',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    ordering = django_filters.OrderingFilter(
        fields = (
            ('vendor__name','vendor'),
        )
    )
    class Meta:
        model = GoodsReceiptNote
        fields = {}


class SalesOrderFilter(django_filters.FilterSet):
    context = {'class':'form-control form-control-sm','onchange':'fetchData(this);enableHighlight();'}
    consumer = django_filters.CharFilter(field_name='consumer__name', lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    date = django_filters.CharFilter(field_name='date',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    so = django_filters.CharFilter(field_name='so',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    ordertotal = django_filters.CharFilter(field_name='ordertotal',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    order_by_field = 'ordering'
    ordering = django_filters.OrderingFilter(
        fields = (
            ('consumer__name','consumer'),
            ('date','date'),
            ('so', 'so'),
            ('ordertotal', 'ordertotal'),
        )
    )
    class Meta:
        model = SalesOrder
        fields = {}


class CompanyFilter(django_filters.FilterSet):
    context = {'class':'form-control form-control-sm','onchange':'fetchData(this);enableHighlight();'}
    name = django_filters.CharFilter(field_name='name', lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    owner = django_filters.CharFilter(field_name='owner',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    phone = django_filters.CharFilter(field_name='phone',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    email = django_filters.CharFilter(field_name='email',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    location = django_filters.CharFilter(field_name='location',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    order_by_field = 'ordering'
    ordering = django_filters.OrderingFilter(
        fields = (
            ('name','name'),
            ('owner','owner'),
            ('phone', 'phone'),
            ('email', 'email'),
            ('location', 'location')
        )
    )
    class Meta:
        model = Company
        fields = {}
        

class EventCardFilter(django_filters.FilterSet):
    context = {'class':'form-control form-control-sm','onkeyup':'fetchEvents()'}
    MODEL_CHOICES = (
        ('Company', 'Company'),
        ('Vendor', 'Vendor'),
        ('PurchaseOrder', 'Purchase Order'),
        ('Product', 'Product'),
        ('Consumer', 'Consumer'),
        ('SalesOrder', 'Sales Order'),
        ('GoodsReceiptNote', 'Goods Receipt Note')
    )
    
    OPERATION_CHOICES = (
        ('Created', 'Created'),
        ('Updated', 'Updated'),
        ('Deleted', 'Deleted')
    )
    objname = django_filters.CharFilter(field_name='objname',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    objmodel = django_filters.MultipleChoiceFilter( choices = MODEL_CHOICES,
                                                    widget=forms.CheckboxSelectMultiple())
    date__gt = django_filters.DateFilter(field_name='date',
                                          lookup_expr= 'date__gt',
                                          widget=forms.TextInput())
    date__lt = django_filters.DateFilter(field_name='date',
                                          lookup_expr= 'date__lt',
                                          widget=forms.TextInput())
    operation = django_filters.MultipleChoiceFilter(choices=OPERATION_CHOICES,
                                                    widget=forms.CheckboxSelectMultiple())
    class Meta:
        model = EventCard
        fields = {}