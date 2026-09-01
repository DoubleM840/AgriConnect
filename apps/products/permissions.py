from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsFarmerOwnerOrReadOnly(BasePermission):
    """
    Anyone (even anonymous) can browse products (GET/HEAD/OPTIONS).
    Only an authenticated farmer can create a listing, and only the
    farmer who owns a listing can edit or delete it.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and request.user.is_farmer)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.farmer_id == request.user.id