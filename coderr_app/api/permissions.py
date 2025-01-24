from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsProviderOrAdmin(BasePermission):
    """
    Only business users can send a POST-Request and admin.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS or request.user.is_superuser:
            return True
        elif request.method == 'POST':
            return request.user.is_authenticated and (request.user.userprofile.type == 'business')
        return False


class IsCustomerOrAdmin(BasePermission):
    """
    Only customers can send a POST-Request and admin.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS or request.user.is_superuser:
            return True
        elif request.method == 'POST':
            return request.user.is_authenticated and (request.user.userprofile.type == 'customer')
        return False


class OrderIsOwnerOrAdmin(BasePermission):
    """
    Only owners from the Order object and admin can send a PATCH-Request. Only admin can send a DELETE-Request.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS or request.user.is_superuser:
            return True
        elif request.method == 'DELETE':
            return request.user.is_authenticated and request.user.is_superuser
        elif request.method == 'PATCH':
            return (request.user.userprofile.type == 'business') and (obj.business_user == request.user)
        else:
            return False


class ReviewIsOwner(BasePermission):
    """
    Only owners from the Review object can send a PATCH- or DELETE-Request.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in ['DELETE', 'PATCH']:
            return request.user.is_authenticated and obj.reviewer == request.user
        return False
