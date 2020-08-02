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

urlpatterns = [
#    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('', views.home, name='home'),
    path('user', views.userPage, name='user-page'),
    path('products/', views.products, name='products'),
    path('invoice/<str:pk>/', views.invoice, name='invoice-path'),
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
]

#for images
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
