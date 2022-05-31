from capstone.pagination import Pagination
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.request import Request
from rest_framework.response import Response

from ideas import serializers

from .models import User
from .permissions import UserRoutesPermissions
from .serializers import LoginSerializer, UserSerializer


class UserView(ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [UserRoutesPermissions]
    queryset = User.objects.all()

    serializer_class = UserSerializer
    pagination_class = Pagination
    
    def paginate_queryset(self, queryset):
        return super().paginate_queryset(queryset)
    

class UserDetailsView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [UserRoutesPermissions]
    queryset = User.objects
    serializer_class = UserSerializer
    lookup_field = "uuid"

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            serializer = self.get_serializer(request.user)
            return Response(serializer.data, 200)

        return super().get(request, *args, **kwargs)


@api_view(["POST"])
def login(request: Request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = authenticate(
        username=serializer.validated_data["email"],
        password=serializer.validated_data["password"],
    )

    if not user:
        return Response({"message": "Invalid password or e-mail address"}, status.HTTP_401_UNAUTHORIZED)

    token, _ = Token.objects.get_or_create(user=user)

    return Response({"token": token.key}, status.HTTP_200_OK)
