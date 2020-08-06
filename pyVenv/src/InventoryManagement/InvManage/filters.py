import django_filters
from .models import *
from django_filters import CharFilter
from django import forms

class ProductFilter(django_filters.FilterSet):
    context = {'class':'form-control form-control-sm','onchange':'fetchData()'}
    name = django_filters.CharFilter(field_name='name', lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    category = django_filters.CharFilter(field_name='category',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    quantity = django_filters.CharFilter(field_name='quantity',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    price = django_filters.CharFilter(field_name='price',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    identifier = django_filters.CharFilter(field_name='identifier',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    location = django_filters.CharFilter(field_name='location',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    class Meta:
        model = Product
        fields = {}

class VendorFilter(django_filters.FilterSet):
    context = {'class':'form-control form-control-sm','onchange':'fetchData()'}
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
    context = {'class':'form-control form-control-sm','onchange':'fetchData()'}
    name = django_filters.CharFilter(field_name='name', lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    identifier = django_filters.CharFilter(field_name='identifier',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    phone = django_filters.CharFilter(field_name='phone',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    email = django_filters.CharFilter(field_name='email',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    location = django_filters.CharFilter(field_name='location',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    class Meta:
        model = Consumer
        fields = {}

class PurchaseOrderFilter(django_filters.FilterSet):
    context = {'class':'form-control form-control-sm','onchange':'fetchData()'}
    vendor = django_filters.CharFilter(field_name='vendor__name', lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    date = django_filters.CharFilter(field_name='date',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    po = django_filters.CharFilter(field_name='po',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    ordertotal = django_filters.CharFilter(field_name='ordertotal',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    class Meta:
        model = PurchaseOrder
        fields = {}
        

class SalesOrderFilter(django_filters.FilterSet):
    context = {'class':'form-control form-control-sm','onchange':'fetchData()'}
    consumer = django_filters.CharFilter(field_name='consumer__name', lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    date = django_filters.CharFilter(field_name='date',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    so = django_filters.CharFilter(field_name='so',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    ordertotal = django_filters.CharFilter(field_name='ordertotal',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    class Meta:
        model = SalesOrder
        fields = {}


class CompanyFilter(django_filters.FilterSet):
    context = {'class':'form-control form-control-sm','onchange':'fetchData()'}
    name = django_filters.CharFilter(field_name='name', lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    owner = django_filters.CharFilter(field_name='owner',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    phone = django_filters.CharFilter(field_name='phone',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    email = django_filters.CharFilter(field_name='email',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    location = django_filters.CharFilter(field_name='location',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
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
        ('SalesOrder', 'Sales Order')
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