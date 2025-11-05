"""
APPLICATION URLs
================
Maps URLs to views for applications.

Includes both:
1. ViewSet URLs (for standard CRUD)
2. Custom apply endpoint
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ApplicationViewSet, apply_for_job

router = DefaultRouter()
router.register(r'applications', ApplicationViewSet, basename='application')

urlpatterns = [
    # Include router URLs for applications
    path('', include(router.urls)),
    
    # Custom endpoint for applying to jobs
    # This creates: POST /apply/
    path('apply/', apply_for_job, name='apply-for-job'),
]

