"""
ANALYTICS VIEWS
===============
This file contains analytics endpoints.

ANALYTICS REQUIREMENTS:
1. Sales summary: Total sales, customers, products sold
2. Top customers: Top 5 customers by purchase amount
3. Top products: Top 5 most sold products

QUERY OPTIMIZATION TECHNIQUES:
- aggregate(): Calculate sum, count, avg, etc.
- annotate(): Add calculated fields to each object
- F expressions: Reference database fields in queries
- select_related/prefetch_related: Reduce queries
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum, Count, F, DecimalField
from django.db.models.functions import Coalesce
from orders.models import Order, OrderItem
from customers.models import Customer
from products.models import Product


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sales_summary(request):
    """
    Get overall sales summary.
    
    Endpoint: GET /api/analytics/sales-summary/
    
    Returns:
    - total_sales: Total revenue (sum of all order totals)
    - total_orders: Number of orders
    - total_customers: Number of customers who placed orders
    - total_products_sold: Total quantity of products sold
    
    Date filtering:
    - ?from=2024-01-01&to=2024-12-31
    """
    
    # Get date filters from query params
    from_date = request.query_params.get('from', None)
    to_date = request.query_params.get('to', None)
    
    # Start with all orders
    orders = Order.objects.all()
    
    # Apply date filters if provided
    if from_date:
        orders = orders.filter(order_date__gte=from_date)
    if to_date:
        orders = orders.filter(order_date__lte=to_date)
    
    # Calculate total sales
    # Sum of (quantity × product price) for all order items
    # F('items__quantity'): Reference the quantity field in related OrderItem
    # F('items__product__price'): Reference the price field in related Product
    total_sales = orders.aggregate(
        total=Coalesce(
            Sum(F('items__quantity') * F('items__product__price'), output_field=DecimalField()),
            0
        )
    )['total']
    
    # Count total orders
    total_orders = orders.count()
    
    # Count unique customers who placed orders (in date range)
    total_customers = orders.values('customer').distinct().count()
    
    # Calculate total quantity of products sold
    total_products_sold = OrderItem.objects.filter(
        order__in=orders
    ).aggregate(
        total=Coalesce(Sum('quantity'), 0)
    )['total']
    
    return Response({
        'total_sales': float(total_sales),
        'total_orders': total_orders,
        'total_customers': total_customers,
        'total_products_sold': total_products_sold,
        'date_range': {
            'from': from_date,
            'to': to_date
        } if (from_date or to_date) else None
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def top_customers(request):
    """
    Get top 5 customers by purchase amount.
    
    Endpoint: GET /api/analytics/top-customers/
    
    Returns list of customers with total_spent, sorted descending.
    
    Date filtering:
    - ?from=2024-01-01&to=2024-12-31
    """
    
    # Get date filters
    from_date = request.query_params.get('from', None)
    to_date = request.query_params.get('to', None)
    
    # Start with all customers
    customers = Customer.objects.all()
    
    # Build the order filter for date range
    order_filter = {}
    if from_date:
        order_filter['orders__order_date__gte'] = from_date
    if to_date:
        order_filter['orders__order_date__lte'] = to_date
    
    # Annotate each customer with their total spending
    # This adds a 'total_spent' field to each customer object
    customers = customers.filter(**order_filter).annotate(
        total_spent=Coalesce(
            Sum(
                F('orders__items__quantity') * F('orders__items__product__price'),
                output_field=DecimalField()
            ),
            0
        )
    ).order_by('-total_spent')[:5]  # Top 5, descending order
    
    # Format response
    result = [
        {
            'id': customer.id,
            'name': customer.name,
            'email': customer.email,
            'total_spent': float(customer.total_spent)
        }
        for customer in customers
    ]
    
    return Response({
        'top_customers': result,
        'date_range': {
            'from': from_date,
            'to': to_date
        } if (from_date or to_date) else None
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def top_products(request):
    """
    Get top 5 most sold products.
    
    Endpoint: GET /api/analytics/top-products/
    
    Returns list of products with total_quantity_sold, sorted descending.
    
    Date filtering:
    - ?from=2024-01-01&to=2024-12-31
    """
    
    # Get date filters
    from_date = request.query_params.get('from', None)
    to_date = request.query_params.get('to', None)
    
    # Start with all products
    products = Product.objects.all()
    
    # Build the order filter for date range
    order_filter = {}
    if from_date:
        order_filter['orderitem__order__order_date__gte'] = from_date
    if to_date:
        order_filter['orderitem__order__order_date__lte'] = to_date
    
    # Annotate each product with total quantity sold
    products = products.filter(**order_filter).annotate(
        total_quantity_sold=Coalesce(Sum('orderitem__quantity'), 0),
        total_revenue=Coalesce(
            Sum(F('orderitem__quantity') * F('price'), output_field=DecimalField()),
            0
        )
    ).order_by('-total_quantity_sold')[:5]  # Top 5
    
    # Format response
    result = [
        {
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'total_quantity_sold': product.total_quantity_sold,
            'total_revenue': float(product.total_revenue)
        }
        for product in products
    ]
    
    return Response({
        'top_products': result,
        'date_range': {
            'from': from_date,
            'to': to_date
        } if (from_date or to_date) else None
    })


# ==============================================================================
# ANALYTICS QUERY EXPLANATION
# ==============================================================================
"""
UNDERSTANDING ANALYTICS QUERIES:

1. aggregate() - Calculate a single value across all records
   Example: Order.objects.aggregate(Sum('items__quantity'))
   Returns: {'items__quantity__sum': 150}

2. annotate() - Add calculated field to each record
   Example: Customer.objects.annotate(total_spent=Sum('orders__items__quantity'))
   Returns: Each customer object now has a 'total_spent' attribute

3. F() - Reference database fields
   Example: F('items__quantity') * F('items__product__price')
   This calculates quantity × price in the database (faster!)

4. Coalesce() - Provide default value if result is NULL
   Example: Coalesce(Sum('quantity'), 0)
   If sum is NULL, return 0 instead

5. select_related() - For foreign keys (1-to-1 or many-to-1)
   Example: Order.objects.select_related('customer')
   Joins customer table in SQL (1 query instead of N+1)

6. prefetch_related() - For many-to-many or reverse foreign keys
   Example: Order.objects.prefetch_related('items__product')
   Does 2 queries (orders, then items+products) instead of N+1

WHY THIS MATTERS:
Without optimization:
- 100 orders = 100 queries (N+1 problem)

With optimization:
- 100 orders = 2-3 queries (much faster!)
"""
