"""
URL configuration for authentication and user profile endpoints.

Defines RESTful routes for:
- User registration and authentication.
- Retrieving and listing user profiles, including business and customer users.

Conventions:
- Uses class-based views for each route.
- All routes are named for reverse URL resolution.

Example usage (reverse):
    reverse('registration')
    reverse('login')
    reverse('user-detail', args=[1])
    reverse('business-user-list')
    reverse('customer-user-list')
"""

from django.urls import path

from .views import RegistrationView, LoginView, UserDetailView, BusinessUserListView, CustomerUserListView

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/<int:user_id>/', UserDetailView.as_view(), name='user-detail'),
    path('profile/business/', BusinessUserListView.as_view(), name='business-user-list'),
    path('profile/customer/', CustomerUserListView.as_view(), name='customer-user-list'),
]
