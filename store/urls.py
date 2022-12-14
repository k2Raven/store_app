"""store URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from webapp.views import ProductList, ProductDetail, ProductCreate, ProductUpdate, ProductDelete, AddItemToCart, \
    CartList, CartDelete, OrderCreate, CartDeleteOne, OrderList

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include("accounts.urls")),
    path('', ProductList.as_view(), name='index'),
    path('product/<int:pk>/view/', ProductDetail.as_view(), name='product_view'),
    path('product/<int:pk>/add_to_cart/', AddItemToCart.as_view(), name='add_to_cart'),
    path('product/<int:pk>/update/', ProductUpdate.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', ProductDelete.as_view(), name='product_delete'),
    path('product/add/', ProductCreate.as_view(), name='product_add'),
    path('cart/', CartList.as_view(), name='cart_index'),
    path('order/', OrderCreate.as_view(), name='order_create'),
    path('order/list/', OrderList.as_view(), name='order_list'),
    path('cart/<str:pk>/delete/', CartDelete.as_view(), name='cart_delete'),
    path('cart/<str:pk>/delete_one/', CartDeleteOne.as_view(), name='cart_delete_one'),
]
