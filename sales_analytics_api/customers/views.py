"""
CUSTOMER VIEWS
==============
Views for managing customers.
"""

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Customer
from .serializers import CustomerSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Customer model.
    
    Provides CRUD operations:
    - GET /api/customers/ - List all customers
    - POST /api/customers/ - Create new customer
    - GET /api/customers/{id}/ - Get specific customer
    - PUT/PATCH /api/customers/{id}/ - Update customer
    - DELETE /api/customers/{id}/ - Delete customer
    """
    
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]
