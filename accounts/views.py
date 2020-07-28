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

    sum = 0
    for product in products:
        sum += product.price * product.amount

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

    myFilter = ProductFilter(request.GET, queryset=products)
    products = myFilter.qs

    context = {'products': products,
    'myFilter': myFilter }

    return render( request, 'accounts/products-new.html', context )

@login_required(login_url='login')
def invoice(request, pk):
    invoice = Invoice.objects.get(id=pk)
    context = {'invoice': invoice}
    return render( request, 'accounts/invoice.html', context )

@login_required(login_url='login')
def addProduct(request):
    form = ProductForm(initial={ 'editor':request.user.username })
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = { 'form': form }
    return render(request, 'accounts/product-form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateProduct(request, pk):
    product = Product.objects.get(id=pk)
    form = ProductForm(initial={'editor' : request.user.username}, instance = product)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance = product)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = { 'form': form }
    return render(request, 'accounts/product-form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteProduct(request, pk):
    item = Product.objects.get(id=pk)

    if request.method == "POST":
        item.delete()
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

    
