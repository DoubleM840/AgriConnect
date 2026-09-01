from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsBuyerOrReadOnly(BasePermission):
    """Only authenticated buyers can create orders; everyone can view their own."""
    
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and request.user.is_buyer

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return obj.buyer == request.user or request.user.is_farmer
        return obj.buyer == request.user