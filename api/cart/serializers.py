from rest_framework import serializers

from shop.serializers import ProductSerializer

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1,21)]

class CartAddProductSerializer(serializers.Serializer):
    quantity = serializers.ChoiceField(choices=PRODUCT_QUANTITY_CHOICES)
    product_id = serializers.IntegerField()

class CartProductSerializer(serializers.Serializer):
    product = ProductSerializer()
    quantity = serializers.IntegerField()
    total_price = serializers.DecimalField(decimal_places=2, max_digits=15)

class CartDetailSerializer(serializers.Serializer):
    products = CartProductSerializer(many=True)
    total_price = serializers.DecimalField(decimal_places=2, max_digits=15)

    class Meta:
        read_only_fields = ['products', 'total_price']
