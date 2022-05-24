from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from .serializers import LoginSerializer


@api_view(["POST"])
def login(request: Request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    print("estou aquiiiiiiiiiiiiiiiiiiiii")
    user = authenticate(username=serializer.validated_data["email"], password=serializer.validated_data["password"])

    if not user:
        return Response({"message": "Invalid password or e-mail address"}, status.HTTP_401_UNAUTHORIZED)

    token, _ = Token.objects.get_or_create(user=user)

    return Response({"token": token.key}, status.HTTP_200_OK)
