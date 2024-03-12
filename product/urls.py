from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from product.apps import ProductConfig
from product.views import CategoriesListAPIView, ProductsListAPIView, CartItemViewSet, CartContentsAPIView, \
    CartClearAPIView

app_name = ProductConfig.name

router = DefaultRouter()
router.register(r'cart-items', CartItemViewSet, basename='cart-items')

urlpatterns = [
    path('categories/', CategoriesListAPIView.as_view(), name='categories-list'),
    path('products/', ProductsListAPIView.as_view(), name='products-list'),
    path('cart-contents/', CartContentsAPIView.as_view(), name='cart-contents'),
    path('cart-clear/', CartClearAPIView.as_view(), name='cart-clear'),

] + router.urls
