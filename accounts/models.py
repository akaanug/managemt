from django.db import models
import datetime
from simple_history.models import HistoricalRecords

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=200)
    barcode = models.CharField(max_length=48)
    code = models.CharField(max_length=255)
    criticalStock = models.BooleanField(default=False) #kritik stok
    criticalStockAmt = models.IntegerField(null=True, blank=True)
    photo = models.ImageField(blank=True, null=True)
    regDate = models.DateTimeField( auto_now_add=True, null=True ) #ürünün kayıt edildiği tarih
    amount = models.IntegerField(blank=True, null=True) #ürünün adeti
    category = models.CharField(max_length=200) #ürünün kategorisi
    brand = models.CharField(max_length = 200) #ürünün markası
    model = models.CharField(max_length = 200, blank=True, null=True)
    description = models.CharField(max_length = 400, blank=True, null=True) #açıklama
    history = HistoricalRecords(
        history_change_reason_field=models.TextField(null=True, max_length=255)
    )

    def __str__(self):
        return f"{self.name} {self.barcode}"

class Invoice(models.Model): #fatura
    invoiceCode = models.CharField( max_length = 200 )
    vendor = models.CharField( max_length=200, blank=True, null=True ) #faturayı kesen firma
    date = models.DateField( blank=True, null=True) #fatura kesim tarihi
    sum = models.FloatField( blank=True, null=True ) #tutar
    taxNo = models.CharField( max_length=200, blank=True, null=True ) #vergi numarası
    history = HistoricalRecords()
    file = models.FileField(blank=True, null=True)

    def __str__(self):
        return f" {self.invoiceCode}"


#records on products in/out
class Logs(models.Model):
    type = models.BooleanField(blank=True, null=True) #True = in, False = out
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    amount = models.IntegerField() #ürünün adeti
    editor = models.CharField(max_length = 200) #giriş/çıkışı kaydeden/silen kullanıcı
    invoice = models.OneToOneField('Invoice', on_delete=models.CASCADE, related_name="fatura", null=True, blank=True )
    logDate = models.DateTimeField( auto_now_add=True, null=True ) #giriş/çıkışın kayıt edildiği tarih
    price = models.FloatField(blank=True, null=True) #giriş/çıkışı yapılan ürünün fiyatı
    company = models.CharField(max_length=200) #alınan/verilen firma
    dateBought = models.DateField(blank=True, null=True) #satın alınan tarih
    productsLeft = models.IntegerField(blank=True, null=True) #Kalan ürün adeti(eğer tip giriş ise)
    lastStocktakeTime = models.DateTimeField(blank=True, null=True) #son sayım yapılan tarih
    history = HistoricalRecords(
        history_change_reason_field=models.TextField(null=True, max_length=255)
    )

    def __str__(self):
        return f" {self.product} {self.type}"
