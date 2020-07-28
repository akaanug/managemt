import django_filters
from django_filters import DateFilter, CharFilter

from .models import *

class ProductFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="dateBought", lookup_expr='gte',
     label='Alış tarihi girilen tarihe eşit ya da ileride olanlar')
    end_date = DateFilter(field_name="dateBought", lookup_expr='lte',
     label='Alış tarihi girilen tarihe eşit ya da geçmişte olanlar')
    name = CharFilter(field_name='name', lookup_expr='icontains', label='Ürün adı')
    description = CharFilter(field_name='description', lookup_expr='icontains',
    label='Açıklama')
    brand = CharFilter(field_name='brand', lookup_expr='icontains', label='Marka')
    category = CharFilter(field_name='category', lookup_expr='icontains', label='Kategori')


    class Meta:
        model = Product
        fields = ['name', 'barcode', 'category', 'brand', 'description',
         'editor', 'vendor']

        labels = {
             'name' : 'Ürün adı',
             'barcode' : 'Barkod',
             'category' : 'Kategori',
             'brand' : 'Marka',
             'description' : 'Açıklama',
             'editor' : 'Kaydeden Kullanıcı',
             'vendor' : 'Alınan Şirket'
         }
