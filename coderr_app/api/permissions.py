from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsProviderOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        elif request.method == 'POST':
            return (request.user.is_authenticated and request.user.is_superuser) or (request.user.is_authenticated and (request.user.userprofile.type == 'business'))
        return False
