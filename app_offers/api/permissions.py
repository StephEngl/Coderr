from rest_framework import permissions
from app_auth.models import UserProfile


class IsBusinessUser(permissions.BasePermission):
    """
    Custom permission to only allow business users to access certain views.
    """

    def has_permission(self, request, view):
        # return request.user and request.user.is_authenticated and getattr(request.user, 'type', None) == 'business'
        if not request.user.is_authenticated:
            return False
        # Richtige Abfrage des Profils!
        try:
            return request.user.userprofile.type == 'business'
        except UserProfile.DoesNotExist:
            return False


class IsOwnerOfOffer(permissions.BasePermission):
    """
    Custom permission to only allow owners of an offer to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user