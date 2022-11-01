from rest_framework import serializers

from shop import models

class CategorySerializer(serializers.ModelSerializer):
    """Serializer for category objects."""

    class Meta:
        model = models.Category
        fields = ('id', 'name', 'slug')
        read_only_fields = ('id',)

class ProductSerializer(serializers.ModelSerializer):
    """Serializer for products."""
    category = CategorySerializer(required=True)

    class Meta:
        model = models.Product
        fields = ['id', 'name', 'category', 'slug', 'price', 'available']
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {
                'lookup_field': 'slug',
            }
        }
        read_only_fields = ('id',)

    def create(self, validated_data):
        """Create a new product."""
        category = validated_data.pop('category', None)
        category_obj, create = models.Category.objects.get_or_create(**category)
        validated_data['category'] = category_obj
        product = models.Product.objects.create(**validated_data)

        return product

    def update(self, instance, validated_data):
        """Update a product."""
        category = validated_data.pop('category', None)
        if category is not None:
            category_obj, create = models.Category.objects.get_or_create(**category)
            setattr(instance, 'category', category_obj)
        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()

        return instance

class ProductDetailSerializer(ProductSerializer):
    """Serializer for product detail view."""
    
    class Meta(ProductSerializer.Meta):
        fields = ProductSerializer.Meta.fields + ['description', 'image']

class ProductImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to products."""

    class Meta:
        model = models.Product
        fields = ['id', 'image']
        read_only_fields = ('id',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {
                'lookup_field': 'slug',
            },
            'image': {
                'required': True
            },
        }