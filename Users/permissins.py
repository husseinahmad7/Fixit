from rest_framework.permissions import BasePermission
from rest_framework.authtoken.models import Token

class HasRolePermission(BasePermission):
    def has_permission(self, request, view):
        token = Token.objects.get(user=request.user)

        return request.user.role == 'admin'
class IsSuperUser(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)
    
class IsUserOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return obj == request.user