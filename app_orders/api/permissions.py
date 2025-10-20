from rest_framework import permissions
from app_auth.models import UserProfile


class IsCustomerUser(permissions.BasePermission):
    """
    Custom permission to only allow customer users to access certain views.
    """
    message = "Only customer users are allowed to perform this action."

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        try:
            return request.user.userprofile.type == 'customer'
        except UserProfile.DoesNotExist:
            return False


class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow admin users to delete orders.
    """
    message = "Only admin users are allowed to delete an order."

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff