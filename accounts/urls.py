"""managemt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

from django.conf.urls.static import static
from django.conf import settings

from django.contrib.auth import views as auth_views

from django.contrib.auth.decorators import login_required

urlpatterns = [
#    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('user', views.userPage, name='user-page'),
    path('invoice/<str:pk>/', views.invoice, name='invoice-path'),
    path('productPage/<str:pk>/', views.productPage, name='productPage'),

    path('listProducts/', views.listProducts, name='listProducts'),

    path('history/<str:pk>/', views.history, name='history-path'),

    path('addProduct/', views.addProduct, name="addProduct"),
    path('updateProduct/<str:pk>', views.updateProduct, name="updateProduct"),
    path('deleteProduct/<str:pk>', views.deleteProduct, name="deleteProduct"),
    path('addInvoice/<str:pk>', views.addInvoice, name="addInvoice"),
    path('updateInvoice/<str:pk>', views.updateInvoice, name="updateInvoice"),
    path('deleteInvoice/<str:pk>', views.deleteInvoice, name="deleteInvoice"),

    path('account/', views.accountSettings, name="account"),

    #to reset the password
    path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
      name="reset_password" ),

    path('reset_password_sent/',
     auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"),
     name="password_reset_done" ),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"),
      name="password_reset_confirm" ),

    path('reset_password_complete/',
     auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"),
      name="password_reset_complete" ),


    path('autocompleteName/', views.autocompleteName, name='autocompleteName'),
    path('autocompleteVendor/', views.autocompleteVendor, name='autocompleteVendor'),
    path('autocompleteCategory/', views.autocompleteCategory, name='autocompleteCategory'),
    path('autocompleteModel/', views.autocompleteModel, name='autocompleteModel'),
    path('autocompleteBrand/', views.autocompleteBrand, name='autocompleteBrand'),

    path('reportPage/', views.report, name='report'),
    path('pdf_view/<str:date>/', login_required(views.ViewPDF.as_view()), name="pdf_view"),
    path('pdf_download/<str:date>/', login_required(views.DownloadPDF.as_view()), name="pdf_download"),

    path('pdf_view/<str:date>/<str:date2>', login_required(views.ViewLogReportPDF.as_view()), name="pdf_log_view"),
    path('pdf_download/<str:date>/<str:date2>', login_required(views.DownloadLogReportPDF.as_view()), name="pdf_log_download"),


    path('view_barcode/', views.barcodeView, name="barcode_view"),
    path('addFromBarcode/', views.addProductFromBarcode, name="addProductFromBarcode"),
    path('addFromBarcode/prefilledAddProduct/<str:pk>/', views.prefilledAddProduct, name="prefilledAddProduct"),

    path('stocktakePage/', views.stocktakePage, name="stocktakePage"),

    path('productST/<int:pk>', views.productSTView, name="productST"),

    path('productEntry/<int:pk>/<int:type>', views.productEntry, name="productEntry"),

    #path('updateStocktakeProduct/<int:pk>', views.StocktakeProductView.as_view(), name='updateStocktakeProduct'),

]

#for images
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
