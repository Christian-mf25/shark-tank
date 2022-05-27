from rest_framework.permissions import BasePermission
from rest_framework.request import Request


class IsInvestorOrSuperuser(BasePermission):
    def has_permission(self, request: Request, _):
        print("anonymous", request.user.is_anonymous)
        print("inv", request.user.is_inv)
        print("superuser", request.user.is_superuser)
        if request.user.is_anonymous:
            return False
        if not request.user.is_inv and not request.user.is_superuser:
            return False
        if request.method == "PATCH" or request.method == "PUT" or request.method == "DELETE":
            return False
        return True
