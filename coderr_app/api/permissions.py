from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsProviderOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS or request.user.is_superuser:
            return True
        elif request.method == 'POST':
            return request.user.is_authenticated and (request.user.userprofile.type == 'business')
        return False


class IsCustomerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS or request.user.is_superuser:
            return True
        elif request.method == 'POST':
            return request.user.is_authenticated and (request.user.userprofile.type == 'customer')
        return False


class OrderIsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS or request.user.is_superuser:
            return True
        elif request.method == 'DELETE':
            return request.user.is_authenticated and request.user.is_superuser
        elif request.method == 'PATCH':
            return (request.user.userprofile.type == 'business') and (obj.business_user == request.user)
        else:
            return False
