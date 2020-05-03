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

class PurchaseOrderFilter(django_filters.FilterSet):
    context = {'class':'form-control form-control-sm','onchange':'fetchData()'}
    vendor = django_filters.CharFilter(field_name='vendor__name', lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    date = django_filters.CharFilter(field_name='date',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    po = django_filters.CharFilter(field_name='po',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    ordertotal = django_filters.CharFilter(field_name='ordertotal',lookup_expr= 'contains',widget=forms.TextInput(attrs=context))
    class Meta:
        model = PurchaseOrder
        fields = {}

class CompanyFilter(django_filters.FilterSet):
    class Meta:
        model = Company
        fields = {'name': ['contains']}