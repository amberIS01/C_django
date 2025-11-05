"""
CUSTOMER SERIALIZER
===================
Serializer for Customer model.
"""

from rest_framework import serializers
from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    """
    Serializer for Customer model.
    
    Includes a custom field showing total amount spent.
    """
    
    # Read-only field showing how much this customer has spent
    total_spent = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True,
        help_text="Total amount spent by this customer"
    )
    
    # Read-only field showing number of orders
    order_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Customer
        fields = ['id', 'name', 'email', 'joined_on', 'total_spent', 'order_count']
        read_only_fields = ['id', 'joined_on']
    
    def get_order_count(self, obj):
        """
        Get number of orders for this customer.
        """
        return obj.orders.count()

