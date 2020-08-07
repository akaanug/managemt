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
    vendor = models.CharField(max_length=200) #alınan firma
    dateBought = models.DateField(null=True) #satın alınan tarih
    regDate = models.DateTimeField( auto_now_add=True, null=True ) #ürünün kayıt edildiği tarih
    price = models.FloatField() #ürünün fiyatı
    amount = models.IntegerField() #ürünün adeti
    category = models.CharField(max_length=200) #ürünün kategorisi
    brand = models.CharField(max_length = 200) #ürünün markası
    model = models.CharField(max_length = 200, blank=True, null=True)
    description = models.CharField(max_length = 400, blank=True, null=True) #açıklama
    editor = models.CharField(max_length = 200) #ürünü kaydeden/silen kullanıcı
    invoice = models.OneToOneField('Invoice', on_delete=models.CASCADE, related_name="fatura", null=True, blank=True )
    history = HistoricalRecords(
        history_change_reason_field=models.TextField(null=True, max_length=255)
    )

    def __str__(self):
        return f"{self.name} {self.barcode} {self.code}"

class Invoice(models.Model): #fatura
    invoiceCode = models.CharField( max_length = 200 )
    vendor = models.CharField( max_length=200, blank=True, null=True ) #faturayı kesen firma
    date = models.DateField( blank=True, null=True) #fatura kesim tarihi
    sum = models.FloatField( blank=True, null=True ) #tutar
    taxNo = models.CharField( max_length=200, blank=True, null=True ) #vergi numarası
    history = HistoricalRecords()

    def __str__(self):
        return f" {self.invoiceCode}"
