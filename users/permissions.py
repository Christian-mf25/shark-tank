from rest_framework.permissions import BasePermission

from .models import User


class IsSuperuser(BasePermission):
    def has_permission(self, request, _):
        user: User = request.user
        is_superuser = request.data.get("is_superuser", False)
        
        if is_superuser and (not user.is_authenticated or not user.is_superuser):
            request.data["is_superuser"] = False
            return True
            
        return True
