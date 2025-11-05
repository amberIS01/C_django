"""
URL configuration for job_application_api project.

MAIN URL ROUTING
================
This file connects URL patterns to app URLs.

URL Structure:
- /admin/ → Django admin panel
- /api/token/ → Get JWT access token
- /api/token/refresh/ → Refresh JWT token
- /api/applicants/ → Applicant endpoints
- /api/jobs/ → Job endpoints
- /api/applications/ → Application endpoints
- /api/apply/ → Apply for a job endpoint
- /media/ → Uploaded files (resumes)
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,  # For getting access and refresh tokens
    TokenRefreshView,     # For refreshing access token
)

urlpatterns = [
    # Django Admin Panel
    # Access at: http://localhost:8000/admin/
    path("admin/", admin.site.urls),
    
    # ==================================================================
    # JWT AUTHENTICATION ENDPOINTS
    # ==================================================================
    # POST /api/token/ with {username, password} → returns {access, refresh} tokens
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # POST /api/token/refresh/ with {refresh} → returns new {access} token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # ==================================================================
    # APP ENDPOINTS
    # ==================================================================
    # Include URLs from each app
    # These use the URL patterns defined in each app's urls.py
    
    # Applicant endpoints: /api/applicants/
    path('api/', include('applicants.urls')),
    
    # Job endpoints: /api/jobs/
    path('api/', include('jobs.urls')),
    
    # Application endpoints: /api/applications/ and /api/apply/
    path('api/', include('applications.urls')),
]

# ==================================================================
# MEDIA FILES (File Uploads)
# ==================================================================
# Serve media files in development
# In production, use nginx or a CDN to serve these
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
