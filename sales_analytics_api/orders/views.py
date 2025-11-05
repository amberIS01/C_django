"""
ORDER VIEWS
===========
Views for managing orders.

QUERY OPTIMIZATION:
We use select_related() and prefetch_related() to reduce database queries.
This is important for performance!
"""

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderListSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Order model.
    
    Uses nested serializer to create orders with items in one request.
    """
    
    # Query optimization:
    # - select_related('customer'): Joins customer table (1-to-1 or foreign key)
    # - prefetch_related('items__product'): Pre-fetches items and their products (many-to-many)
    # This reduces database queries from N+1 to just 3 queries!
    queryset = Order.objects.select_related('customer').prefetch_related('items__product').all()
    
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        """
        Use different serializers for list vs detail views.
        
        - List view: Use lighter serializer (OrderListSerializer)
        - Detail/Create/Update: Use full serializer (OrderSerializer)
        
        This improves performance for list views.
        """
        if self.action == 'list':
            return OrderListSerializer
        return OrderSerializer
    
    def get_queryset(self):
        """
        Optionally filter orders by customer or date range.
        
        Examples:
        - /api/orders/?customer=5
        - /api/orders/?from=2024-01-01&to=2024-12-31
        """
        queryset = super().get_queryset()
        
        # Filter by customer
        customer_id = self.request.query_params.get('customer', None)
        if customer_id:
            queryset = queryset.filter(customer_id=customer_id)
        
        # Filter by date range
        from_date = self.request.query_params.get('from', None)
        to_date = self.request.query_params.get('to', None)
        
        if from_date:
            queryset = queryset.filter(order_date__gte=from_date)
        if to_date:
            queryset = queryset.filter(order_date__lte=to_date)
        
        return queryset
