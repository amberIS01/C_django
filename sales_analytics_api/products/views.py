"""
PRODUCT VIEWS
=============
Views for managing products.
"""

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Product model.
    
    Provides CRUD operations:
    - GET /api/products/ - List all products
    - POST /api/products/ - Create new product
    - GET /api/products/{id}/ - Get specific product
    - PUT/PATCH /api/products/{id}/ - Update product
    - DELETE /api/products/{id}/ - Delete product
    """
    
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
