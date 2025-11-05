"""
ANALYTICS URLs
==============
Maps URLs to analytics views.

These are function-based views, so we use path() instead of routers.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Sales summary endpoint
    path('analytics/sales-summary/', views.sales_summary, name='sales-summary'),
    
    # Top customers endpoint
    path('analytics/top-customers/', views.top_customers, name='top-customers'),
    
    # Top products endpoint
    path('analytics/top-products/', views.top_products, name='top-products'),
]

