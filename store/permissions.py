from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
     return bool (request.method=="GET") or (request.user and request.user.is_staff)

        #  if request.method in permissions.SAFE_METHODS:
        #     return True
        # return bool (request.user and request.user.is_staff)