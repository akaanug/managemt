import django_filters
from django_filters import DateFilter, CharFilter

from .models import *

class ProductFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains', label='Ürün adı')
    barcode = CharFilter(field_name='description', lookup_expr='icontains',
    label='Barkod')


    class Meta:
        model = Product
        fields = ['name', 'barcode']

        labels = {
             'name' : 'Ürün adı',
             'barcode' : 'Barkod',
         }
