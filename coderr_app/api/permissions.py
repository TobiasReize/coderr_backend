from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        elif request.user:
            return (obj.user == request.user) or request.user.is_superuser
        else:
            return False


class IsProvider(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        elif request.method == 'POST':
            return request.user.is_authenticated and (request.user__type == 'business')
        return False
