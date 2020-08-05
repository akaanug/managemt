from django.forms import ModelForm
from .models import *
from django import forms
from django.forms import DateInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__' #create form with all of the fields in Product

        widgets = {
            'name' : forms.TextInput(attrs={'placeholder': 'Ürün adını gir', }),
            'dateBought': DateInput(attrs={'type': 'date', }),
            'editor': forms.HiddenInput(),
        }

        labels = {
            'name' : 'Ürün adı',
            'barcode' : 'Barkod',
            'code' : 'Ürün Kodu',
            'criticalStock' : 'Kritik Stok',
            'criticalStockAmt' : 'Kritik Stok Sayısı',
            'photo' : 'Ürününün Fotoğrafı',
            'vendor' : 'Alınan Firma',
            'dateBought' : 'Alış Tarihi',
            'price' : 'Alış Fiyatı',
            'amount' : 'Stoktaki Miktar',
            'category' : 'Kategori',
            'brand' : 'Marka',
            'model' : 'Model',
            'description' : 'Açıklama',
            'editor' : 'Kaydeden Kullanıcı',
        }

        exclude = ( 'invoice', )

class InvoiceForm(ModelForm):
    class Meta:
        model = Invoice
        fields = ['invoiceCode', 'date', 'sum', 'taxNo']

        labels = {
            'invoiceCode' : 'Fatura Kodu',
            'date' : 'Fatura Kesim Tarihi',
            'sum' : 'Toplam Tutar',
            'taxNo' : 'Vergi Numarası',
        }


class AccountForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', ]
