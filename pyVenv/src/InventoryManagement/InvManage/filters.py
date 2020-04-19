import django_filters
from .models import *
from django_filters import CharFilter
from django import forms

class ProductFilter(django_filters.FilterSet):
    # desc = CharFilter(field_name='description', lookup_expr='icontains')
    context = {'class':'form-control form-control-sm'}
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
    class Meta:
        model = Vendor
        fields = {'name': ['contains']}

class PurchaseOrderFilter(django_filters.FilterSet):
    class Meta:
        model = PurchaseOrder
        fields = {  'po': ['contains'],
                    'vendor__name': ['contains'],
                    'date':['contains'],
                    'subtotal':['contains'],
                    'taxtotal':['contains'],
                    'ordertotal':['contains']}

class CompanyFilter(django_filters.FilterSet):
    class Meta:
        model = Company
        fields = {'name': ['contains']}