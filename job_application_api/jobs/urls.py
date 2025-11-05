"""
JOB URLs
========
Maps URLs to views for jobs.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobViewSet

router = DefaultRouter()
router.register(r'jobs', JobViewSet, basename='job')

urlpatterns = router.urls

