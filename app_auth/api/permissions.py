from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.exceptions import NotFound, ValidationError, PermissionDenied

class IsProfileOwner(BasePermission):
    """
    Custom permission to only allow owners of a profile to edit it.
    """
    message = "You have to be the owner of this profile to edit it."

    def has_object_permission(self, request, view, obj):
        is_profile_owner = obj.user == request.user
        if request.method in SAFE_METHODS:
            return True
        return is_profile_owner