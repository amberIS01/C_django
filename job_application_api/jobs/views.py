"""
JOB VIEWS
=========
Views for managing job postings.
"""

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Job
from .serializers import JobSerializer


class JobViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Job model.
    
    Provides CRUD operations for jobs:
    - GET /api/jobs/ - List all jobs
    - POST /api/jobs/ - Create new job
    - GET /api/jobs/{id}/ - Get specific job
    - PUT/PATCH /api/jobs/{id}/ - Update job
    - DELETE /api/jobs/{id}/ - Delete job
    """
    
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Optionally filter jobs by title.
        
        Example: /api/jobs/?title=developer
        
        This method is called to get the queryset for the view.
        We can customize it to add filters.
        """
        queryset = super().get_queryset()
        
        # Get 'title' parameter from URL query string
        title = self.request.query_params.get('title', None)
        
        if title:
            # Filter jobs where title contains the search term (case-insensitive)
            queryset = queryset.filter(title__icontains=title)
        
        return queryset
