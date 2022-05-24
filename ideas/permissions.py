from rest_framework.permissions import BasePermission
from rest_framework.request import Request


class CreateOrRead(BasePermission):
    def has_permission(self, request: Request, _):
        if request.user.is_anonymous:
            return False
        if request.method == "POST" and not request.user.is_inv and not request.user.is_adm:
            return True
        if request.method == "GET" and request.user.is_inv:
            return True
        return False

class OwnerRead(BasePermission):
    def has_object_permission(self, request: Request, _):
        if request.user.is_anonymous:
            return False
        if request.method == "GET" and not request.user.is_inv and not request.user.is_adm:
            return True
        return False