"""
CUSTOMER MODEL
==============
This file defines the Customer model for the Sales Analytics API.

Customers are people who buy products (create orders).
"""

from django.db import models


class Customer(models.Model):
    """
    Stores customer information.
    
    A customer can place multiple orders.
    """
    
    name = models.CharField(
        max_length=100,
        help_text="Customer's full name"
    )
    
    email = models.EmailField(
        unique=True,
        help_text="Unique email address"
    )
    
    joined_on = models.DateTimeField(
        auto_now_add=True,
        help_text="When the customer registered"
    )
    
    class Meta:
        ordering = ['-joined_on']  # Newest customers first
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
    
    def __str__(self):
        return f"{self.name} ({self.email})"
    
    @property
    def total_spent(self):
        """
        Calculate total amount this customer has spent.
        
        This is a property - you can access it like: customer.total_spent
        It calculates the value on-demand.
        """
        from orders.models import Order
        from django.db.models import Sum, F
        
        # Get all orders for this customer
        # Calculate total: sum of (quantity * product.price) for all order items
        total = Order.objects.filter(customer=self).aggregate(
            total=Sum(F('items__quantity') * F('items__product__price'))
        )['total']
        
        return total or 0  # Return 0 if no orders
