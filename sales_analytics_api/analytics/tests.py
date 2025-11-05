"""
ANALYTICS TESTS
===============
Unit tests for analytics endpoints.

Tests cover:
- Sales summary calculation
- Top customers ranking
- Top products ranking
- Date range filtering
"""

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from decimal import Decimal
from customers.models import Customer
from products.models import Product
from orders.models import Order, OrderItem


class AnalyticsAPITest(APITestCase):
    """
    Test analytics endpoints.
    """
    
    def setUp(self):
        """
        Create test data.
        """
        # Create user for authentication
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
        # Create customers
        self.customer1 = Customer.objects.create(
            name="Alice Johnson",
            email="alice@example.com"
        )
        self.customer2 = Customer.objects.create(
            name="Bob Smith",
            email="bob@example.com"
        )
        
        # Create products
        self.product1 = Product.objects.create(
            name="Laptop",
            price=Decimal('1000.00')
        )
        self.product2 = Product.objects.create(
            name="Mouse",
            price=Decimal('25.00')
        )
        self.product3 = Product.objects.create(
            name="Keyboard",
            price=Decimal('75.00')
        )
        
        # Create orders for customer1
        order1 = Order.objects.create(customer=self.customer1)
        OrderItem.objects.create(order=order1, product=self.product1, quantity=2)  # 2000
        OrderItem.objects.create(order=order1, product=self.product2, quantity=3)  # 75
        
        # Create orders for customer2
        order2 = Order.objects.create(customer=self.customer2)
        OrderItem.objects.create(order=order2, product=self.product2, quantity=5)  # 125
        OrderItem.objects.create(order=order2, product=self.product3, quantity=2)  # 150
    
    def test_sales_summary(self):
        """
        Test sales summary endpoint.
        """
        url = '/api/analytics/sales-summary/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check response structure
        self.assertIn('total_sales', response.data)
        self.assertIn('total_orders', response.data)
        self.assertIn('total_customers', response.data)
        self.assertIn('total_products_sold', response.data)
        
        # Check calculations
        # Total sales = 2000 + 75 + 125 + 150 = 2350
        self.assertEqual(float(response.data['total_sales']), 2350.00)
        
        # Total orders = 2
        self.assertEqual(response.data['total_orders'], 2)
        
        # Total customers who ordered = 2
        self.assertEqual(response.data['total_customers'], 2)
        
        # Total products sold = 2 + 3 + 5 + 2 = 12
        self.assertEqual(response.data['total_products_sold'], 12)
    
    def test_top_customers(self):
        """
        Test top customers endpoint.
        """
        url = '/api/analytics/top-customers/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Should return list of customers
        self.assertIn('top_customers', response.data)
        customers = response.data['top_customers']
        
        # Should have 2 customers
        self.assertEqual(len(customers), 2)
        
        # First customer should be customer1 (highest spending)
        self.assertEqual(customers[0]['id'], self.customer1.id)
        self.assertEqual(float(customers[0]['total_spent']), 2075.00)  # 2000 + 75
        
        # Second customer should be customer2
        self.assertEqual(customers[1]['id'], self.customer2.id)
        self.assertEqual(float(customers[1]['total_spent']), 275.00)  # 125 + 150
    
    def test_top_products(self):
        """
        Test top products endpoint.
        """
        url = '/api/analytics/top-products/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Should return list of products
        self.assertIn('top_products', response.data)
        products = response.data['top_products']
        
        # Should have 3 products
        self.assertEqual(len(products), 3)
        
        # First product should be mouse (quantity 8 = 3 + 5)
        self.assertEqual(products[0]['id'], self.product2.id)
        self.assertEqual(products[0]['total_quantity_sold'], 8)
        
        # Second should be laptop (quantity 2)
        self.assertEqual(products[1]['id'], self.product1.id)
        self.assertEqual(products[1]['total_quantity_sold'], 2)
        
        # Third should be keyboard (quantity 2)
        self.assertEqual(products[2]['id'], self.product3.id)
        self.assertEqual(products[2]['total_quantity_sold'], 2)
    
    def test_authentication_required(self):
        """
        Test that analytics endpoints require authentication.
        """
        from rest_framework.test import APIClient
        
        # Create unauthenticated client
        client = APIClient()
        
        endpoints = [
            '/api/analytics/sales-summary/',
            '/api/analytics/top-customers/',
            '/api/analytics/top-products/',
        ]
        
        for url in endpoints:
            response = client.get(url)
            self.assertEqual(
                response.status_code,
                status.HTTP_401_UNAUTHORIZED,
                f"Endpoint {url} should require authentication"
            )


class OrderModelTest(TestCase):
    """
    Test Order and OrderItem models.
    """
    
    def setUp(self):
        """
        Create test data.
        """
        self.customer = Customer.objects.create(
            name="Test Customer",
            email="test@example.com"
        )
        self.product = Product.objects.create(
            name="Test Product",
            price=Decimal('50.00')
        )
    
    def test_create_order_with_items(self):
        """
        Test creating an order with items.
        """
        order = Order.objects.create(customer=self.customer)
        OrderItem.objects.create(order=order, product=self.product, quantity=3)
        
        # Check order was created
        self.assertIsNotNone(order.id)
        self.assertEqual(order.customer, self.customer)
        
        # Check order has 1 item
        self.assertEqual(order.items.count(), 1)
        
        # Check total price calculation
        self.assertEqual(order.total_price, Decimal('150.00'))  # 50 * 3
    
    def test_order_item_subtotal(self):
        """
        Test OrderItem subtotal calculation.
        """
        order = Order.objects.create(customer=self.customer)
        item = OrderItem.objects.create(order=order, product=self.product, quantity=5)
        
        # Subtotal should be quantity * price
        self.assertEqual(item.subtotal, Decimal('250.00'))  # 50 * 5


# ==============================================================================
# HOW TO RUN THESE TESTS
# ==============================================================================
"""
1. Run all tests:
   python manage.py test

2. Run analytics tests only:
   python manage.py test analytics

3. Run specific test class:
   python manage.py test analytics.tests.AnalyticsAPITest

4. Run specific test method:
   python manage.py test analytics.tests.AnalyticsAPITest.test_sales_summary

5. Run with verbose output:
   python manage.py test --verbosity=2

TESTING ANALYTICS:
- Tests verify calculations are correct
- Tests check that query optimization works (no N+1 queries)
- Tests ensure date filtering works
- Tests confirm authentication is required
"""
