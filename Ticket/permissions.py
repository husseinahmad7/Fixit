from rest_framework.permissions import BasePermission

class OwnerOrAdminPermission(BasePermission):
    """
    Custom permission to allow only clients, staff, and superusers to update tickets.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False

        # Allow clients, staff, and superusers to update their own tickets
        return obj.client == request.user or request.user.is_staff or request.user.is_superuser

class TicketPictureOwnerOrAdminPermission(BasePermission):
    """
    Custom permission to allow only clients, staff, and superusers to update tickets.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False

        # Allow clients, staff, and superusers to update their own tickets
        return obj.ticket.client == request.user or request.user.is_staff or request.user.is_superuser
