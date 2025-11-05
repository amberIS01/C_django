"""
JOB SERIALIZER
==============
Serializer for Job model - converts between Job objects and JSON.
"""

from rest_framework import serializers
from .models import Job


class JobSerializer(serializers.ModelSerializer):
    """
    Serializer for the Job model.
    Handles conversion between Job model instances and JSON.
    """
    
    # Custom read-only field showing how many applications this job has
    # SerializerMethodField: Calls get_<field_name>() method to get value
    application_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ['id', 'posted_on']
    
    def get_application_count(self, obj):
        """
        Calculate number of applications for this job.
        
        Args:
            obj: The Job instance being serialized
            
        Returns:
            Number of applications for this job
        """
        # obj.applications is the related name from Application model
        # .count() efficiently counts without loading all records
        return obj.applications.count()

