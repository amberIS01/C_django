"""
CUSTOMER URLs
=============
Maps URLs to customer views.
"""

from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet

router = DefaultRouter()
router.register(r'customers', CustomerViewSet, basename='customer')

urlpatterns = router.urls

