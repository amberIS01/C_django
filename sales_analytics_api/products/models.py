"""
PRODUCT MODEL
=============
This file defines the Product model for the Sales Analytics API.

Products are items that customers can purchase.
"""

from django.db import models


class Product(models.Model):
    """
    Stores product information.
    
    Products have a name and price.
    They can be included in many orders (via OrderItem).
    """
    
    name = models.CharField(
        max_length=100,
        help_text="Product name"
    )
    
    # DecimalField: For money/prices (more accurate than FloatField)
    # max_digits=10: Total number of digits (including decimals)
    # decimal_places=2: Number of decimal places (e.g., 99.99)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Product price"
    )
    
    class Meta:
        ordering = ['name']  # Alphabetical order
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
    
    def __str__(self):
        return f"{self.name} (${self.price})"
