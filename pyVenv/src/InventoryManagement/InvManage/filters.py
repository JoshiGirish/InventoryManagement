import django_filters
from .models import *
from django_filters import CharFilter

class ProductFilter(django_filters.FilterSet):
    # desc = CharFilter(field_name='description', lookup_expr='icontains')
    class Meta:
        model = Product
        fields = {'description': ['contains']}
