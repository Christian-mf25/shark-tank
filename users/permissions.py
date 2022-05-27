from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission
from rest_framework.request import Request


class UserRoutesPermissions(BasePermission):
    def has_permission(self, request: Request, _):
        
        if request.method == "POST":
            is_superuser: bool = request.data.get("is_superuser", False)

            if is_superuser and (not request.user.is_authenticated or not request.user.is_superuser):
                raise PermissionDenied("Only admin can create a superuser.")

            if is_superuser:
                request.data["is_staff"] = True
    
            return True

        if request.method == "GET":
            if not request.user.is_authenticated:
                return False

        return True
