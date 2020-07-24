import django_filters
from .models import *
from django_filters import CharFilter
from django import forms

class ProductFilter(django_filters.FilterSet):
    # desc = CharFilter(field_name='description', lookup_expr='icontains')
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
    phone = django_filters.CharFilter(field_name='phone',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    email = django_filters.CharFilter(field_name='email',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    location = django_filters.CharFilter(field_name='location',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    class Meta:
        model = Vendor
        fields = {}
        
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
    # obj = django_filters.CharFilter(field_name='name', lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    # objId = django_filters.CharFilter(field_name='owner',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    objname = django_filters.CharFilter(field_name='objname',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    # objmodel = django_filters.CharFilter(field_name='email',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    # date = django_filters.CharFilter(field_name='location',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    # operation = django_filters.CharFilter(field_name='location',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    class Meta:
        model = EventCard
        fields = {}