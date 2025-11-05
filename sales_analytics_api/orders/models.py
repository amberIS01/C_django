"""
ORDER AND ORDER ITEM MODELS
============================
This file defines the Order and OrderItem models.

RELATIONSHIPS:
- Customer → Order: One-to-many (one customer can have many orders)
- Order → OrderItem: One-to-many (one order can have many items)
- Product → OrderItem: One-to-many (one product can be in many order items)

Think of it like a shopping cart:
- Order = The shopping cart
- OrderItem = Individual items in the cart (product + quantity)
"""

from django.db import models
from django.core.validators import MinValueValidator
from customers.models import Customer
from products.models import Product


class Order(models.Model):
    """
    Represents a customer's order.
    
    An order can contain multiple products (via OrderItem).
    """
    
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='orders',  # Access customer's orders: customer.orders.all()
        help_text="The customer who placed this order"
    )
    
    order_date = models.DateTimeField(
        auto_now_add=True,
        help_text="When the order was placed"
    )
    
    class Meta:
        ordering = ['-order_date']  # Newest orders first
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
    
    def __str__(self):
        return f"Order #{self.id} by {self.customer.name}"
    
    @property
    def total_price(self):
        """
        Calculate total price of this order.
        
        Total = sum of (quantity × product price) for all items
        
        This is a property, so you can access it like: order.total_price
        """
        total = sum(item.subtotal for item in self.items.all())
        return total
    
    def save(self, *args, **kwargs):
        """
        Override save to add validation.
        
        save() is called when you create or update an object.
        We override it to add custom logic.
        """
        super().save(*args, **kwargs)
        
        # After saving, check if order has at least one item
        # (This only applies to existing orders, not during creation)
        if self.pk and not self.items.exists():
            # Note: We can't enforce this in save() for new orders
            # We'll enforce it in the serializer instead
            pass


class OrderItem(models.Model):
    """
    Represents a single item in an order.
    
    This is the "many-to-many through" model between Order and Product.
    It stores additional data (quantity) about the relationship.
    """
    
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',  # Access order's items: order.items.all()
        help_text="The order this item belongs to"
    )
    
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        help_text="The product being ordered"
    )
    
    # IntegerField with validation: quantity must be >= 1
    quantity = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1)],  # Must be at least 1
        help_text="Quantity of this product"
    )
    
    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'
    
    def __str__(self):
        return f"{self.quantity}x {self.product.name} in Order #{self.order.id}"
    
    @property
    def subtotal(self):
        """
        Calculate subtotal for this item.
        
        Subtotal = quantity × product price
        """
        return self.quantity * self.product.price
