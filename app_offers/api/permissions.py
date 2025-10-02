from rest_framework import permissions


class IsBusinessUser(permissions.BasePermission):
    """
    Custom permission to only allow business users to access certain views.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and getattr(request.user, 'type', None) == 'business'


class IsOwnerOfOffer(permissions.BasePermission):
    """
    Custom permission to only allow owners of an offer to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user