"""
APPLICANT URLs
==============
Maps URLs to views for applicants.

Django REST Framework provides routers that automatically create URL patterns
for ViewSets.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ApplicantViewSet

# Create a router - this automatically generates URL patterns for ViewSets
# DefaultRouter includes:
# - List view: GET /applicants/
# - Create view: POST /applicants/
# - Detail view: GET /applicants/{id}/
# - Update view: PUT /applicants/{id}/
# - Partial update: PATCH /applicants/{id}/
# - Delete view: DELETE /applicants/{id}/

router = DefaultRouter()

# Register the viewset with the router
# 'applicants' is the base name (used in URL patterns)
# ApplicantViewSet is the view to use
router.register(r'applicants', ApplicantViewSet, basename='applicant')

# Include the router URLs
urlpatterns = router.urls

