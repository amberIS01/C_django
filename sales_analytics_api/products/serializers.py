"""
PRODUCT SERIALIZER
==================
Serializer for Product model.
"""

from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for Product model.
    """
    
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['id']
    
    def validate_price(self, value):
        """
        Ensure price is positive.
        """
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value

