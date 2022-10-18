from rest_framework.authentication import TokenAuthentication
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from drf_spectacular.utils import extend_schema_view

from core import permissions
from shop import serializers, models

@extend_schema_view()
class ProductViewSet(ModelViewSet):
    """API view for managing products."""
    serializer_class = serializers.ProductDetailSerializer
    queryset = models.Product.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAdminOrReadOnly]
    lookup_field = 'slug'

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.ProductSerializer
        elif self.action == 'upload_image':
            return serializers.ProductImageSerializer

        return self.serializer_class

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image for the product."""
        product = self.get_object()
        serializer = self.get_serializer(product, data=request.data)
        
        if serializer.is_valid():
            serializer.save(product=product)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

class CategoryViewSet(ModelViewSet):
    """API view for managing categories."""
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAdminOrReadOnly]
    lookup_field = 'slug'