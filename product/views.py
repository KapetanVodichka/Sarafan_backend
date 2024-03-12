from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from product.models import Category, Product, CartItem, Cart
from product.paginators import CategoriesPagination, ProductsPagination
from product.permissions import IsOwner
from product.serializers import CategorySerializer, ProductSerializer, CartItemSerializer


class CategoriesListAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CategoriesPagination
    permission_classes = [AllowAny]


class ProductsListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductsPagination
    permission_classes = [AllowAny]


class CartItemViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsOwner]

    def create(self, request):
        user_cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartItemSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(cart=user_cart)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        cart_item = get_object_or_404(CartItem, pk=pk)
        serializer = CartItemSerializer(cart_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        cart_item = get_object_or_404(CartItem, pk=pk)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartContentsAPIView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def get(self, request):
        cart_items = CartItem.objects.filter(cart__user=request.user)
        grouped_items = cart_items.values('product').annotate(quantity=Count('product'))
        total_price = 0

        for item in grouped_items:
            product_id = item['product']
            product = Product.objects.get(pk=product_id)
            item['product_name'] = product.name
            item['product_price'] = product.price
            total_price += product.price * item['quantity']

        return Response({'cart_items': grouped_items, 'total_price': total_price})


class CartClearAPIView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def post(self, request):
        cart_items = CartItem.objects.filter(cart__user=request.user)
        cart_items.delete()

        return Response({'message': 'Корзина очищена'}, status=204)