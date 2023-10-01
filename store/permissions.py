from rest_framework import permissions
from rest_framework.permissions import BasePermission

class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
     return bool (request.method=="GET") or (request.user and request.user.is_staff)

        #  if request.method in permissions.SAFE_METHODS:
        #     return True
        # return bool (request.user and request.user.is_staff)

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow read-only permissions for any request
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        # Allow write permissions only if the user is the owner of the comment
        return obj.user == request.user
