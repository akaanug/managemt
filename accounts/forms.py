from django.forms import ModelForm
from .models import *
from django import forms
from django.forms import DateInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from bootstrap_modal_forms.forms import BSModalModelForm

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
            'lastStocktakeTime': forms.HiddenInput(),
        }

        labels = {
            'name' : 'Ürün adı',
            'barcode' : 'Barkod',
            'code' : 'Ürün Kodu',
            'criticalStock' : 'Kritik Stok',
            'criticalStockAmt' : 'Kritik Stok Sayısı',
            'photo' : 'Ürününün Fotoğrafı',
            'amount' : 'Stoktaki Miktar',
            'category' : 'Kategori',
            'brand' : 'Marka',
            'model' : 'Model',
            'description' : 'Açıklama',
            'editor' : 'Kaydeden Kullanıcı',
        }

        exclude = ( 'invoice', 'amount' )

class InvoiceForm(ModelForm):
    class Meta:
        model = Invoice
        fields = ['invoiceCode', 'date', 'sum', 'taxNo', 'file']

        labels = {
            'invoiceCode' : 'Fatura Kodu',
            'date' : 'Fatura Kesim Tarihi',
            'sum' : 'Toplam Tutar',
            'taxNo' : 'Vergi Numarası',
            'file': 'Fatura Dosyası'
        }


class AccountForm(ModelForm):
    class Meta:
        model = User
        fields = [ 'username', 'email', ]

class ProductSTForm(ModelForm):
    class Meta:
        model = Logs
        fields = ['productsLeft', 'lastStocktakeTime']

        widgets = {'lastStocktakeTime': forms.HiddenInput(),}

        labels = {
            'productsLeft' : 'Kalan Adet',
            'lastStocktakeTime' : "",
        }


class TransactionForm(ModelForm):
    class Meta:
        model = Logs
        fields = ['amount', 'price', 'dateBought', 'company']

        widgets = {
            'type': forms.HiddenInput(),
            'dateBought': DateInput(attrs={'type': 'date', }),
        }

        labels = {
            'amount' : 'Adet',
            'price' : 'Birim Fiyatı',
            'company' : 'Satın alınan/ürünün verildiği Firma',
            'dateBought' : 'Satın Alma/Verme Tarihi',
        }

        exclude = ( 'invoice', )


'''
class StocktakeModelForm(BSModalModelForm):
    class Meta:
        model = Product
        fields = ['amount',]
'''
