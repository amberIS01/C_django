"""
APPLICANT VIEWS
===============
Views handle HTTP requests and return responses.

KEY CONCEPTS:
- ViewSet: A class that provides CRUD operations (list, create, retrieve, update, delete)
- Queryset: The set of database records this view works with
- Serializer: Converts between models and JSON
- Filters: For searching and filtering data
"""

from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import Applicant
from .serializers import ApplicantSerializer


class ApplicantViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Applicant model.
    
    ModelViewSet automatically provides:
    - list(): GET /api/applicants/ - List all applicants
    - create(): POST /api/applicants/ - Create new applicant
    - retrieve(): GET /api/applicants/{id}/ - Get specific applicant
    - update(): PUT /api/applicants/{id}/ - Update applicant
    - partial_update(): PATCH /api/applicants/{id}/ - Partial update
    - destroy(): DELETE /api/applicants/{id}/ - Delete applicant
    """
    
    # Queryset: What database records this view can access
    # .all() means all applicants (will be filtered by search if needed)
    queryset = Applicant.objects.all()
    
    # Serializer: How to convert between Applicant objects and JSON
    serializer_class = ApplicantSerializer
    
    # Permission: Who can access this view
    # IsAuthenticated: Must have valid JWT token
    permission_classes = [IsAuthenticated]
    
    # Search functionality: Allows ?search=john or ?search=john@example.com
    filter_backends = [filters.SearchFilter]
    
    # Search fields: Which fields to search in
    # '^name' means "starts with" search on name
    # 'email' means "contains" search on email
    search_fields = ['name', 'email']
    
    # You can also use:
    # '^name' - starts with
    # '=name' - exact match
    # '@name' - full-text search
    # 'name' - contains (default)
