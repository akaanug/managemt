from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from .filters import ProductFilter
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.models import Group
from django.http import JsonResponse


from xhtml2pdf import pisa
from django.views import View
from django.template.loader import get_template
from io import BytesIO
from django.utils import timezone
from datetime import datetime as dt

import simple_history
from simple_history.utils import update_change_reason

import pytz

from bootstrap_modal_forms.generic import BSModalUpdateView
from django.urls import reverse_lazy

#from django.core.mail import EmailMessage
#from django.conf import settings
#from django.template.loader import render_to_string


#sends information email to admin every week that contains criticalProducts etc.
#def sendInformationEmail(request):
#    template = render_to_string('accounts/email_template.html', { 'products' : products })


"""
@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            email = form.cleaned_data.get('email')

            group = Group.objects.get(name='kullanıcı')
            user.groups.add(group)

            messages.success(request, email + ' email adresiyle başarıyla kayıt olundu.')

            return redirect('login')

    context = { 'form':form }
    return render(request, 'accounts/register.html', context)
"""


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Kullanıcı adı ya da şifre hatalı.')

    context = {}
    return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def home(request):
    products = Product.objects.all()
    invoices = Invoice.objects.all()
    criticalProducts = []
    outOfStock = []

    for product in products:
        if product.criticalStock and product.criticalStockAmt != None and product.amount <= product.criticalStockAmt:
            criticalProducts.append(product)
        if product.amount == 0:
            outOfStock.append(product)

    start = 5
    if products.count() <= 5:
        start = 0
    else:
        start = products.count() - 5

    context = { 'products': products[ start :], 'invoices': invoices, 'sum': sum,
                'criticalProducts': criticalProducts, 'outOfStock' : outOfStock }
    return render( request, 'accounts/dashboard.html',  context )

def userPage(request):
    context = {}
    return render(request, 'accounts/user.html', context)

@login_required(login_url='login')
def products(request):
    products = Product.objects.all()
    context = {'products': products }

    return render( request, 'accounts/products-new.html', context )

@login_required(login_url='login')
def invoice(request, pk):
    invoice = Invoice.objects.get(id=pk)
    context = {'invoice': invoice}
    return render( request, 'accounts/invoice.html', context )

@login_required(login_url='login')
def addProduct(request):
    productForm = ProductForm(initial={ 'editor':request.user.username, })
    invoiceForm = InvoiceForm()
    if request.method == 'POST':
        invoiceForm = InvoiceForm(request.POST)
        productForm = ProductForm(request.POST, request.FILES)
        if invoiceForm.is_valid() and productForm.is_valid():
            newProduct = productForm.save()
            update_change_reason(newProduct, "Ürün eklendi.")
            newInvoice = invoiceForm.save()

            #fill invoice based on information in newProduct
            sum = newProduct.price * newProduct.amount
            newInvoice.sum = sum
            newInvoice.vendor = newProduct.vendor
            newInvoice.date = newProduct.dateBought
            newInvoice.save()

            #link invoice to product
            newProduct.invoice = newInvoice
            newProduct.save()
            update_change_reason(newProduct, "Fatura eklendi.")

            successMessage = str(newProduct.name) + " adlı ürün başarıyla eklendi."
            messages.success(request, successMessage)
            return redirect('/')
        else:
            message = "Ürün eklenemedi."
            messages.warning(request, message)

    context = { 'productForm': productForm, 'invoiceForm': invoiceForm }
    return render(request, 'accounts/product-form.html', context)


#get change of last two histories as string
def getHistoryLabel(product):

    #translate English labels to Turkish
    translateDict = {
        "name": "Ürün Adı",
        "barcode": "Barkod",
        "code": "Ürün Kodu",
        "regDate":"Kayıt Tarihi",
        "price" : "Fiyat",
        "amount" : "Adet",
        "category": "Kategori",
        "brand": "Marka",
        "model": "Model",
        "description" : "Açıklama",
        "editor": "Düzenleyen Kullanıcı",
        "photo": "Fotoğraf",
        "vendor": "Alınan Şirket",
        "criticalStock": "Kritik Stok",
        "criticalStockAmt" : "Kritik Stok Sayısı",
        "dateBought": "Alış Tarihi",
        "invoice": "Fatura",
        "history": "Tarih",
        "lastStocktakeTime": "Son Sayım Tarihi",
    }

    histories = product.history.all()

    #get last record
    new_record = histories.first()
    #get older record
    old_record = new_record.prev_record

    delta = new_record.diff_against(old_record)

    s = ""
    for change in delta.changes:
        if change.field == "lastStocktakeTime":
            oldTime = change.old
            if oldTime is None:
                oldTime = "Hiç"
            else:
                oldTime = change.old.strftime("%Y-%m-%d %H:%M")
            newTime = change.new.strftime("%Y-%m-%d %H:%M")
            s += ("{}, {} iken {} olarak değiştirildi. ".format(translateDict[change.field],
            oldTime, newTime))
        else:
            s += ("{}, {} iken {} olarak değiştirildi. ".format(translateDict[change.field],
            change.old, change.new))

    return s



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateProduct(request, pk):
    product = Product.objects.get(id=pk)
    productForm = ProductForm(initial={'editor' : request.user.username}, instance = product)
    invoiceForm = InvoiceForm(instance = product.invoice)
    if request.method == 'POST':
        productForm = ProductForm(request.POST, request.FILES, instance = product)
        invoiceForm = InvoiceForm( request.POST, instance = product.invoice )
        if productForm.is_valid() and invoiceForm.is_valid():
            productForm.save()
            update_change_reason(product, getHistoryLabel(product))
            invoiceForm.save()

            successMessage = str(product.name) + " adlı ürün başarıyla güncellendi."
            messages.success(request, successMessage)
            return redirect('/products/')
        else:
            successMessage = str(product.name) + " adlı ürün güncellenemedi."
            messages.warning(request, failedMessage)


    context = { 'productForm': productForm, 'invoiceForm': invoiceForm }
    return render(request, 'accounts/product-form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteProduct(request, pk):
    item = Product.objects.get(id=pk)

    if request.method == "POST":
        item.delete()

        successMessage = str(item.name) + " adlı ürün başarıyla silindi."
        messages.success(request, successMessage)

        return redirect('/')

    context = {'item': item}
    return render(request, 'accounts/delete.html', context)

@login_required(login_url='login')
def addInvoice(request, pk):
    item = Product.objects.get(id=pk)
    sum = item.price * item.amount

    form = InvoiceForm(initial={ 'vendor':item.vendor, 'sum': sum, 'date': item.dateBought })
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            form.save()
            item.invoice = form.save()
            item.invoice.vendor = item.vendor
            item.invoice.save()
            item.save()
            return redirect('/')

    context = { 'form': form, 'item' : item }
    return render(request, 'accounts/invoice-form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateInvoice(request, pk):
    invoice = Invoice.objects.get(id=pk)
    form = InvoiceForm(instance = invoice)

    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance = invoice)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = { 'form': form }
    return render(request, 'accounts/invoice-form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteInvoice(request, pk):
    item = Invoice.objects.get(id=pk)

    if request.method == "POST":
        item.delete()
        return redirect('/')

    context = {'item': item}
    return render(request, 'accounts/deleteInvoice.html', context)


@login_required(login_url='login')
def accountSettings(request):
    user = request.user
    form = AccountForm(instance=request.user)

    if request.method == 'POST':
        form = AccountForm(request.POST, instance=user)
        if form.is_valid():
            form.save()

    context = {'form':form}
    return render(request, 'accounts/account-settings.html',context )

def autocompleteName(request):
    if 'term' in request.GET:
        qs = Product.objects.filter(name__istartswith=request.GET.get('term'))
        names = list()
        for product in qs:
            if product.name not in names:
                names.append(product.name)
        # titles = [product.title for product in qs]
        return JsonResponse(names, safe=False)
    return render(request, 'accounts/product-form.html')


def autocompleteVendor(request):
    if 'term' in request.GET:
        qs = Product.objects.filter(vendor__istartswith=request.GET.get('term'))
        vendors = list()
        for product in qs:
            if product.vendor not in vendors:
                vendors.append(product.vendor)

        # titles = [product.title for product in qs]
        return JsonResponse(vendors, safe=False)
    return render(request, 'accounts/product-form.html')


def autocompleteCategory(request):
    if 'term' in request.GET:
        qs = Product.objects.filter(category__istartswith=request.GET.get('term'))
        categories = list()
        for product in qs:
            if product.category not in categories:
                categories.append(product.category)

        # titles = [product.title for product in qs]
        return JsonResponse(categories, safe=False)
    return render(request, 'accounts/product-form.html')


def autocompleteModel(request):
    if 'term' in request.GET:
        qs = Product.objects.filter(model__istartswith=request.GET.get('term'))
        models = list()

        for product in qs:
            if product.model not in models:
                models.append(product.model)

        # titles = [product.title for product in qs]
        return JsonResponse(models, safe=False)
    return render(request, 'accounts/product-form.html')


def autocompleteBrand(request):
    if 'term' in request.GET:
        qs = Product.objects.filter(brand__istartswith=request.GET.get('term'))
        brands = list()

        for product in qs:
            if product.brand not in brands:
                brands.append(product.brand)
        # titles = [product.title for product in qs]
        return JsonResponse(brands, safe=False)
    return render(request, 'accounts/product-form.html')


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


#Opens up page as PDF
class ViewPDF(View):
    def get(self, request, *args, **kwargs):

        utc = pytz.UTC

        #pass date parameter as string and convert it back to datetime.datetime
        date = kwargs['date']
        dateObj = dt.strptime(date, '%Y-%m-%d')

        #dateObj points to the end of the day
        time = datetime.time(23,59,59)
        endOfTheDay = dt.combine(dateObj, time)

        #get all products in specified date
        qs = Product.objects.filter(regDate__lte=endOfTheDay)

        products = []

        #get an instance of the model as it would
        #have existed at the provided date
        for product in qs:
            hist = None

            #if product is not created yet
            try:
                hist = product.history.as_of(endOfTheDay)
            except Exception as ex:
                print(ex)

            if hist is not None:
                products.append( hist )

        sum = 0
        for product in products:
            sum += product.price * product.amount

        #get beginning of the day in order to find all operations in that day
        time = datetime.time(0,0,0)
        beginningOfTheDay = dt.combine(dateObj, time)

        allHistories = []

        #By default, the datetime object is naive in Python, so you need to
        #make both of them either naive or aware datetime objects.
        #This can be done using:
        beginningOfTheDay = utc.localize(beginningOfTheDay)
        endOfTheDay = utc.localize(endOfTheDay)

        #Get all processes made in chosen day
        allProducts = Product.objects.all()
        for product in allProducts:
            productHistories = product.history.all()

            for history in productHistories:
                if (history.history_date >= beginningOfTheDay) and (history.history_date <= endOfTheDay):
                    allHistories.append(history)

        products = {
            'products': products,
            'sum': sum,
            'date': date,
            'allHistories': allHistories,
        }

        pdf = render_to_pdf('accounts/pdf_template.html', products)
        return HttpResponse(pdf, content_type='application/pdf')


#Automaticly downloads to PDF file
class DownloadPDF(View):
    def get(self, request, *args, **kwargs):

        #pass date parameter as string and convert it back to datetime.datetime
        utc = pytz.UTC

        #pass date parameter as string and convert it back to datetime.datetime
        date = kwargs['date']
        dateObj = dt.strptime(date, '%Y-%m-%d')

        #dateObj points to the end of the day
        time = datetime.time(23,59,59)
        endOfTheDay = dt.combine(dateObj, time)

        #get all products in specified date
        qs = Product.objects.filter(regDate__lte=endOfTheDay)

        products = []

        #get an instance of the model as it would
        #have existed at the provided date
        for product in qs:
            hist = None

            #if product is not created yet
            try:
                hist = product.history.as_of(endOfTheDay)
            except Exception as ex:
                print(ex)

            if hist is not None:
                products.append( hist )

        sum = 0
        for product in products:
            sum += product.price * product.amount

        #get beginning of the day in order to find all operations in that day
        time = datetime.time(0,0,0)
        beginningOfTheDay = dt.combine(dateObj, time)

        allHistories = []

        #By default, the datetime object is naive in Python, so you need to
        #make both of them either naive or aware datetime objects.
        #This can be done using:
        beginningOfTheDay = utc.localize(beginningOfTheDay)
        endOfTheDay = utc.localize(endOfTheDay)

        #Get all processes made in chosen day
        allProducts = Product.objects.all()
        for product in allProducts:
            productHistories = product.history.all()

            for history in productHistories:
                if (history.history_date >= beginningOfTheDay) and (history.history_date <= endOfTheDay):
                    allHistories.append(history)

        products = {
            'products': products,
            'sum': sum,
            'date': date,
            'allHistories': allHistories,
        }

        pdf = render_to_pdf('accounts/pdf_template.html', products)
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "DTS_Rapor_%s.pdf" %(date)
        content = "attachment; filename=%s" %(filename)
        response['Content-Disposition'] = content
        return response

@login_required(login_url='login')
def report(request):
    current_date = dt.today().date()
    date = current_date

    if request.method=="POST":
        date = request.POST.get('date')

    context = { 'date' : date }
    return render(request, 'accounts/reportPage.html', context)


@login_required(login_url='login')
def history(request, pk):
    product = Product.objects.get(id=pk)
    histories = product.history.all()
    context = {'histories': histories}
    return render( request, 'accounts/history.html', context )


@login_required(login_url='login')
def barcodeView(request):
    barcodeInstance = None
    if request.method=="POST":
        barcodeInstance = request.POST.get('barcode')
        productSet = None

        #get the product with scanned barcode
        try:
            productSet = Product.objects.filter(barcode=barcodeInstance)
        except Exception as ex:
            print(ex)

        #if there is more than one product with given barcode
        if productSet.count() > 1:
            context = {'barcode': barcodeInstance, 'products': productSet}
            return render(request, 'accounts/listProducts.html', context )

        #if there is only one product with scanned barcode
        if productSet.count() == 1:
            product = productSet[0]
            pk = product.id
            return productPage(request, pk)
        else:
            context = {'barcode':barcodeInstance}
            return render(request, 'accounts/product404.html', context )

    return render(request, 'accounts/readBarcode.html')



@login_required(login_url='login')
def productPage(request, pk):
    product = Product.objects.get(id=pk)
    context = {'product': product}
    return render( request, 'accounts/productPage.html', context )

@login_required(login_url='login')
def listProducts(request):
    return render( request, 'accounts/listProducts.html' )


#prefill form with the information of the product which has the scanned barcode
@login_required(login_url='login')
def addProductFromBarcode(request):
    barcodeInstance = None
    if request.method=="POST":
        barcodeInstance = request.POST.get('barcode')
        product = None

        #get the product with scanned barcode
        try:
            product = Product.objects.filter(barcode=barcodeInstance)[0]
        except Exception as ex:
            print(ex)
            #if there is no product, give 404 error
            context = {'barcode' : barcodeInstance}
            return render(request, 'accounts/product404.html', context )

        #insert barcode as parameter via the URL
        return redirect( 'prefilledAddProduct/{}'.format(barcodeInstance) )

    return render(request, 'accounts/readBarcode.html')


#return prefilled product form
@login_required(login_url='login')
def prefilledAddProduct(request, pk):

    barcodeInstance = pk
    product = Product.objects.filter(barcode=barcodeInstance)[0]
    productForm = ProductForm(initial={ 'editor': request.user.username,
                                        'name': product.name,
                                        'vendor': product.vendor,
                                        'barcode': product.barcode,
                                        'category': product.category,
                                        'brand': product.brand,
                                        'model': product.model,
                                        'description': product.description,
                                        'photo': product.photo,
                                        'code': product.code })
    invoiceForm = InvoiceForm()
    if request.method == 'POST':
        invoiceForm = InvoiceForm(request.POST)
        productForm = ProductForm(request.POST, request.FILES)
        if invoiceForm.is_valid() and productForm.is_valid() :
            newProduct = productForm.save()
            update_change_reason(newProduct, "Ürün eklendi.")
            newInvoice = invoiceForm.save()

            #fill invoice based on information in newProduct
            sum = newProduct.price * newProduct.amount
            newInvoice.sum = sum
            newInvoice.vendor = newProduct.vendor
            newInvoice.date = newProduct.dateBought
            newInvoice.save()

            #link invoice to product
            newProduct.invoice = newInvoice
            newProduct.save()
            update_change_reason(newProduct, "Fatura eklendi.")

            message = str(newProduct.name) + " adlı ürün başarıyla eklendi."
            messages.success(request, message)
            return redirect('/')
        else:
            message = str(product.name) + " adlı ürün eklenemedi."
            messages.warning(request, message)

    context = { 'productForm': productForm, 'invoiceForm': invoiceForm }
    return render(request, 'accounts/product-form.html', context)


@login_required(login_url='login')
def stocktakePage(request):
    dateObj = timezone.now()
    time = datetime.time(0,0,0)
    beginningOfTheDay = dt.combine(dateObj, time)

    stocktakeProducts = Product.objects.filter(
        lastStocktakeTime__isnull=False
    ).filter(
        lastStocktakeTime__gt=beginningOfTheDay
    )

    nullST = Product.objects.filter(lastStocktakeTime__isnull=True)
    lteToday = Product.objects.filter(lastStocktakeTime__lte=beginningOfTheDay)
    products = nullST | lteToday

    productFilter = ProductFilter(request.GET, queryset=products)
    products = productFilter.qs

    context = { 'stocktakeProducts': stocktakeProducts, 'products': products,
     'productFilter': productFilter, }

    return render(request, 'accounts/stocktakePage.html', context)

@login_required(login_url='login')
def productSTView(request, pk):
    product = Product.objects.get(id=pk)
    productForm = ProductSTForm(initial={'lastStocktakeTime': timezone.now()},
     instance = product )
    if request.method == 'POST':
        productForm = ProductSTForm(request.POST, instance = product)
        oldAmt = product.amount
        if productForm.is_valid():
            productForm.save()
            newAmt = product.amount

            #find loss if any
            loss = 0
            if oldAmt <= newAmt:
                loss = 0
            else:
                loss = (oldAmt - newAmt) * product.price

            if loss == 0:
                r = "Zarar Yok."
            else:
                r = str(oldAmt - newAmt) + " adet ürün eksik. Zarar = " + str(loss) + " TL."

            reason = "SAYIM: " + getHistoryLabel(product) + r

            update_change_reason(product, reason)

            message = str(product.name) + " adlı ürünün sayımı başarılı."
            messages.success(request, message)
            return redirect('/stocktakePage/')
        else:
            message = str(product.name) + " adlı ürünün sayımı başarısız."
            messages.warning(request, message)

    context = { 'form': productForm, }
    return render(request, 'accounts/updateStocktakeProduct.html', context)


'''
class StocktakeProductView(BSModalUpdateView):
    model = Product
    template_name = 'accounts/updateStocktakeProduct.html'
    form_class = StocktakeModelForm
    success_message = 'Sayım Başarılı!'
    success_url = reverse_lazy('stocktakePage')
'''
