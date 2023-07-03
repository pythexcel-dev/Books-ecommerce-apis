from rest_framework import permissions 


class IsSelfUser(permissions.BasePermission):
    """
    Custom permission to only allow access to the user itself.
    """
    def has_permission(self, request, view):
        return request.user.id == view.kwargs.get('user_id')
    

class IsVendorOnly(permissions.BasePermission):
    """
    Custom permission to only allow access to the user itself.
    """
    def has_permission(self, request, view):
        return request.user.user_role == 'Vendor'
