"""
APPLICANT SERIALIZER
====================
Serializers convert between Python objects (models) and JSON data.

HOW IT WORKS:
1. Client sends JSON → Serializer validates → Creates/Updates model
2. Model exists → Serializer converts → Sends JSON to client

Think of serializers as translators between JSON (API) and Django models (database).
"""

from rest_framework import serializers
from .models import Applicant


class ApplicantSerializer(serializers.ModelSerializer):
    """
    Serializer for the Applicant model.
    
    ModelSerializer automatically:
    - Creates fields based on the model
    - Handles validation
    - Provides create() and update() methods
    """
    
    class Meta:
        """
        Meta class tells the serializer:
        - Which model to use
        - Which fields to include
        - Any additional options
        """
        model = Applicant
        
        # '__all__' includes all model fields
        # Alternative: fields = ['id', 'name', 'email', ...] for specific fields
        fields = '__all__'
        
        # read_only_fields: These fields are sent in response but not accepted in requests
        read_only_fields = ['id', 'applied_on']  # Auto-generated, can't be set by user
    
    def validate_email(self, value):
        """
        Custom validation for email field.
        
        This method is automatically called when validating email.
        Method name pattern: validate_<field_name>
        
        Args:
            value: The email value to validate
            
        Returns:
            The validated email (lowercase)
            
        Raises:
            ValidationError: If validation fails
        """
        # Convert email to lowercase for consistency
        return value.lower()
    
    def validate_phone(self, value):
        """
        Custom validation for phone field.
        Ensures phone number contains only digits, spaces, +, -, ()
        """
        if value:  # Only validate if phone is provided (it's optional)
            # Remove common formatting characters
            cleaned = value.replace(' ', '').replace('-', '').replace('(', '').replace(')', '').replace('+', '')
            
            if not cleaned.isdigit():
                raise serializers.ValidationError(
                    "Phone number should only contain digits and +, -, (, ) characters."
                )
        
        return value

