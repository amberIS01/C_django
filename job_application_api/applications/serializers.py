"""
APPLICATION SERIALIZERS
=======================
This file contains serializers for job applications.

IMPORTANT CONCEPTS:
1. ModelSerializer: Automatically creates fields from model
2. Custom validation: Prevents duplicate applications
3. Nested serialization: Shows full applicant/job details in responses
"""

from rest_framework import serializers
from .models import Application
from applicants.serializers import ApplicantSerializer
from jobs.serializers import JobSerializer


class ApplicationSerializer(serializers.ModelSerializer):
    """
    Serializer for Application model.
    Shows full applicant and job details in GET requests.
    """
    
    # When reading (GET), show full details using nested serializers
    # When writing (POST/PUT), only need to send IDs
    applicant_details = ApplicantSerializer(source='applicant', read_only=True)
    job_details = JobSerializer(source='job', read_only=True)
    
    class Meta:
        model = Application
        fields = [
            'id',
            'applicant',           # ID only (for creating/updating)
            'applicant_details',   # Full details (in responses)
            'job',                 # ID only (for creating/updating)
            'job_details',         # Full details (in responses)
            'status',
            'applied_on'
        ]
        read_only_fields = ['id', 'applied_on']
    
    def validate(self, data):
        """
        Object-level validation - validates multiple fields together.
        
        This is called after individual field validation.
        We use it to check if applicant already applied for this job.
        
        Args:
            data: Dictionary of all validated field data
            
        Returns:
            The validated data
            
        Raises:
            ValidationError: If applicant already applied for this job
        """
        # Check if this is a new application (not an update)
        if not self.instance:  # instance is None for new objects
            applicant = data.get('applicant')
            job = data.get('job')
            
            # Check if application already exists
            # EXISTS() is efficient - returns True/False without loading data
            if Application.objects.filter(applicant=applicant, job=job).exists():
                raise serializers.ValidationError(
                    "This applicant has already applied for this job. Duplicate applications are not allowed."
                )
        
        return data


class ApplySerializer(serializers.Serializer):
    """
    Special serializer for the /api/apply/ endpoint.
    
    This is NOT a ModelSerializer because we want custom behavior:
    - Takes applicant_id and job_id
    - Creates an Application automatically
    - Returns success message with application details
    """
    
    # These fields accept IDs, not full objects
    applicant_id = serializers.IntegerField(
        help_text="ID of the applicant applying for the job"
    )
    job_id = serializers.IntegerField(
        help_text="ID of the job to apply for"
    )
    
    def validate_applicant_id(self, value):
        """
        Validate that applicant exists.
        """
        from applicants.models import Applicant
        
        try:
            Applicant.objects.get(id=value)
        except Applicant.DoesNotExist:
            raise serializers.ValidationError(f"Applicant with ID {value} does not exist.")
        
        return value
    
    def validate_job_id(self, value):
        """
        Validate that job exists.
        """
        from jobs.models import Job
        
        try:
            Job.objects.get(id=value)
        except Job.DoesNotExist:
            raise serializers.ValidationError(f"Job with ID {value} does not exist.")
        
        return value
    
    def validate(self, data):
        """
        Check for duplicate application.
        """
        from applicants.models import Applicant
        from jobs.models import Job
        
        applicant = Applicant.objects.get(id=data['applicant_id'])
        job = Job.objects.get(id=data['job_id'])
        
        # Check if already applied
        if Application.objects.filter(applicant=applicant, job=job).exists():
            raise serializers.ValidationError(
                f"{applicant.name} has already applied for {job.title}. Duplicate applications are not allowed."
            )
        
        return data
    
    def create(self, validated_data):
        """
        Create the application.
        
        This method is called when you call serializer.save()
        """
        from applicants.models import Applicant
        from jobs.models import Job
        
        applicant = Applicant.objects.get(id=validated_data['applicant_id'])
        job = Job.objects.get(id=validated_data['job_id'])
        
        # Create and return the application
        application = Application.objects.create(
            applicant=applicant,
            job=job,
            status='applied'  # Default status
        )
        
        return application

