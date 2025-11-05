"""
URL configuration for sales_analytics_api project.

SALES ANALYTICS API - MAIN URLS
================================

URL Structure:
- /admin/ → Django admin panel
- /api/token/ → Get JWT access token
- /api/token/refresh/ → Refresh JWT token
- /api/customers/ → Customer endpoints
- /api/products/ → Product endpoints
- /api/orders/ → Order endpoints (with nested items)
- /api/analytics/sales-summary/ → Total sales analytics
- /api/analytics/top-customers/ → Top 5 customers
- /api/analytics/top-products/ → Top 5 products
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Django Admin
    path("admin/", admin.site.urls),
    
    # JWT Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # App endpoints
    path('api/', include('customers.urls')),
    path('api/', include('products.urls')),
    path('api/', include('orders.urls')),
    path('api/', include('analytics.urls')),
]
