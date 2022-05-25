from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from .models import User
from .permissions import IsSuperuser
from .serializers import LoginSerializer, UserSerializer


class UserView(ListCreateAPIView):
    authenticate_classes = [TokenAuthentication]
    permission_classes = [IsSuperuser]
    queryset = User.objects.all()

    serializer_class = UserSerializer


@api_view(["POST"])
def login(request: Request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = authenticate(
        username=serializer.validated_data["email"].lower(), password=serializer.validated_data["password"]
    )

    if not user:
        return Response({"message": "Invalid password or e-mail address"}, status.HTTP_401_UNAUTHORIZED)

    token, _ = Token.objects.get_or_create(user=user)

    return Response({"token": token.key}, status.HTTP_200_OK)
