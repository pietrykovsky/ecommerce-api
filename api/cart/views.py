from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema

from shop.models import Product
from .cart import Cart
from . import serializers

from decimal import Decimal

@extend_schema(
    responses=serializers.CartDetailSerializer
)
@api_view(['GET'])
def cart_detail(request):
    """Show cart details."""
    cart = Cart(request)
    data = cart.get_details()
    serializer = serializers.CartDetailSerializer(data)
    return Response(serializer.data, status=status.HTTP_200_OK)

@extend_schema(
    request=serializers.CartAddProductSerializer,
    responses= serializers.CartAddProductSerializer
)
@api_view(['POST', 'PUT'])
def cart_add(request):
    """Add or update quantity of the product in the cart."""
    serializer = serializers.CartAddProductSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        product_id = data['product_id']
        quantity = data['quantity']
        product = get_object_or_404(Product, pk=product_id)
        cart = Cart(request)

        if request.method == 'POST':
            cart.add(product=product, quantity=quantity)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            cart.add(product=product, quantity=quantity, update_quantity=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema()
@api_view(['DELETE'])
def cart_remove(request, product_id):
    """Remove a product from the cart."""
    cart = Cart(request)
    product = get_object_or_404(Product, pk=product_id)
    cart.remove(product)
    return Response(status=status.HTTP_204_NO_CONTENT)

@extend_schema()
@api_view(['DELETE'])
def cart_clear(request):
    """Clear the cart."""
    cart = Cart(request)
    cart.clear()
    return Response(status=status.HTTP_204_NO_CONTENT)