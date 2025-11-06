"""
URL configuration for meta-related endpoints.

Defines RESTful routes for:
- Retrieving basic application meta information.

Conventions:
- Uses class-based views for each route.
- Includes explicit route names for reverse URL resolution.

Example usage (reverse):
    reverse('base-info')
"""

from django.urls import path

from .views import BaseInfoView


urlpatterns = [
    path('base-info/', BaseInfoView.as_view(), name='base-info')
]
