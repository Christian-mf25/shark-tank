from rest_framework.permissions import BasePermission
from rest_framework.request import Request


class IsInvestor(BasePermission):
    def has_permission(self, request: Request, _):
        if request.user.is_anonymous:
            return False
        if not request.user.is_inv:
            return False
        if request.method == "PATCH" or request.method == "PUT" or request.method == "DELETE":
            return False
        return True
