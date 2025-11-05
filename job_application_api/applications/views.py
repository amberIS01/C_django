"""
APPLICATION VIEWS
=================
Views for managing job applications.

This file includes:
1. ApplicationViewSet - For viewing and updating applications
2. ApplyView - Special endpoint for creating applications
"""

from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Application
from .serializers import ApplicationSerializer, ApplySerializer


class ApplicationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Application model.
    
    Note: We override some methods to customize behavior
    """
    
    queryset = Application.objects.select_related('applicant', 'job').all()
    # select_related: Optimization technique that reduces database queries
    # Instead of 1 query for applications + N queries for related applicant/job,
    # it does 1 query that JOINs all tables together (much faster!)
    
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Optionally filter applications by status or applicant.
        
        Examples:
        - /api/applications/?status=shortlisted
        - /api/applications/?applicant=5
        """
        queryset = super().get_queryset()
        
        # Filter by status
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by applicant ID
        applicant_id = self.request.query_params.get('applicant', None)
        if applicant_id:
            queryset = queryset.filter(applicant_id=applicant_id)
        
        # Filter by job ID
        job_id = self.request.query_params.get('job', None)
        if job_id:
            queryset = queryset.filter(job_id=job_id)
        
        return queryset
    
    def create(self, request, *args, **kwargs):
        """
        Override create to provide better error messages.
        """
        serializer = self.get_serializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def apply_for_job(request):
    """
    Special endpoint for job applications.
    
    Endpoint: POST /api/apply/
    
    Request body:
    {
        "applicant_id": 1,
        "job_id": 2
    }
    
    This is a function-based view (not a class-based ViewSet).
    Function-based views are simpler for single-purpose endpoints.
    
    Decorators:
    - @api_view(['POST']): Marks this as a DRF API view, only accepts POST
    - @permission_classes([IsAuthenticated]): Requires JWT authentication
    """
    
    # Create serializer with request data
    serializer = ApplySerializer(data=request.data)
    
    # Validate the data
    if serializer.is_valid():
        # Save (calls serializer.create())
        application = serializer.save()
        
        # Return success response with full application details
        response_serializer = ApplicationSerializer(application)
        
        return Response({
            'message': 'Application submitted successfully',
            'application': response_serializer.data
        }, status=status.HTTP_201_CREATED)
    
    # If validation fails, return errors
    return Response({
        'error': 'Application failed',
        'details': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)
