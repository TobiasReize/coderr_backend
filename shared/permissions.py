from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrAdmin(BasePermission):
    """
    Checks whether the logged in user is the owner or admin.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS or request.user.is_superuser:
            return True
        elif request.user:
            return obj.user == request.user
        else:
            return False
