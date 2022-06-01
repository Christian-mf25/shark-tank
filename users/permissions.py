from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission
from rest_framework.request import Request


class UserRoutesPermissions(BasePermission):
    def has_permission(self, request: Request, _):
        if request.method == 'PATCH':
            if str(request.user.uuid) == str(request.build_absolute_uri()[32:-1]):
                print(request.data)
                request.data["is_superuser"] = request.user.is_superuser
                return True     
            
        methods = ("POST", "PATCH")
        if request.method in methods:
            is_superuser: bool = request.data.get("is_superuser", False)

            if is_superuser and (not request.user.is_authenticated or not request.user.is_superuser):
                raise PermissionDenied("Only admin can create or update a superuser.")

            if is_superuser:
                request.data["is_staff"] = True

            return True

        if request.method == "GET":
            if not request.user.is_authenticated or not request.user.is_superuser:
                return False

        return True
