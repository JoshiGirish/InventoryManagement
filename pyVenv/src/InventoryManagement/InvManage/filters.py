import django_filters
from .models import *
from django_filters import CharFilter

class ProductFilter(django_filters.FilterSet):
    # desc = CharFilter(field_name='description', lookup_expr='icontains')
    class Meta:
        model = Product
        fields = {'name': ['contains']}

class VendorFilter(django_filters.FilterSet):
    class Meta:
        model = Vendor
        fields = {'name': ['contains']}

class PurchaseOrderFilter(django_filters.FilterSet):
    class Meta:
        model = PurchaseOrder
        fields = {'vendor__name': ['contains']}

class CompanyFilter(django_filters.FilterSet):
    class Meta:
        model = Company
        fields = {'name': ['contains']}