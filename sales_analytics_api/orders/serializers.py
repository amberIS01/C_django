"""
ORDER SERIALIZERS
=================
This file contains serializers for Order and OrderItem models.

KEY CONCEPT: NESTED SERIALIZERS
When creating an order, we want to include the items in the same request:
{
    "customer": 1,
    "items": [
        {"product": 1, "quantity": 2},
        {"product": 2, "quantity": 1}
    ]
}

This requires nested serializers.
"""

from rest_framework import serializers
from .models import Order, OrderItem
from customers.serializers import CustomerSerializer
from products.serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer for OrderItem model.
    
    Shows product details in responses.
    """
    
    # In responses, show full product details
    product_details = ProductSerializer(source='product', read_only=True)
    
    # Calculate and include subtotal
    subtotal = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_details', 'quantity', 'subtotal']
        read_only_fields = ['id', 'subtotal']
    
    def validate_quantity(self, value):
        """
        Ensure quantity is at least 1.
        """
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1.")
        return value


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for Order model with nested items.
    
    NESTED CREATION:
    When creating an order, you can include items:
    {
        "customer": 1,
        "items": [
            {"product": 1, "quantity": 2},
            {"product": 2, "quantity": 1}
        ]
    }
    """
    
    # For responses: show full customer details
    customer_details = CustomerSerializer(source='customer', read_only=True)
    
    # For nested creation/update of items
    # This allows creating order items within the order creation request
    items = OrderItemSerializer(many=True)
    
    # Calculate and include total price
    total_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    
    class Meta:
        model = Order
        fields = ['id', 'customer', 'customer_details', 'order_date', 'items', 'total_price']
        read_only_fields = ['id', 'order_date', 'total_price']
    
    def validate_items(self, value):
        """
        Validate that order has at least one item.
        """
        if not value:
            raise serializers.ValidationError("Order must have at least one item.")
        return value
    
    def create(self, validated_data):
        """
        Create order with nested items.
        
        This method is called when you call serializer.save()
        
        Process:
        1. Extract items data from validated_data
        2. Create the order
        3. Create each order item
        4. Return the order
        """
        # Extract items data (remove from validated_data)
        items_data = validated_data.pop('items')
        
        # Create the order (without items)
        order = Order.objects.create(**validated_data)
        
        # Create each order item
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        
        return order
    
    def update(self, instance, validated_data):
        """
        Update order with nested items.
        
        Process:
        1. Extract items data
        2. Update order fields
        3. Delete existing items
        4. Create new items
        5. Return updated order
        """
        # Extract items data if present
        items_data = validated_data.pop('items', None)
        
        # Update order fields (customer, etc.)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # If items data was provided, update items
        if items_data is not None:
            # Delete existing items
            instance.items.all().delete()
            
            # Create new items
            for item_data in items_data:
                OrderItem.objects.create(order=instance, **item_data)
        
        return instance


class OrderListSerializer(serializers.ModelSerializer):
    """
    Lighter serializer for listing orders (without full nested data).
    
    Use this for list views to improve performance.
    Use OrderSerializer for detail views.
    """
    
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    item_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = ['id', 'customer', 'customer_name', 'order_date', 'total_price', 'item_count']
        read_only_fields = ['id', 'order_date']
    
    def get_item_count(self, obj):
        """
        Get number of items in this order.
        """
        return obj.items.count()

