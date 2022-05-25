from capstone.exceptions import CustomException
from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("uuid", "name", "email", "password", "phone", "is_inv")
        extra_kwargs = {"uuid": {"read_only": True}, "password": {"write_only": True}}

        def validate(self, attrs):
            user: User = self.context["request"].user
            attrs["name"] = attrs["name"].title()
            attrs["email"] = attrs["email"].swapcase()

        def create(self, validated_data):
            if validated_data["is_superuser"] and (user.is_authenticated and user.is_superuser):
                if validated_data["is_superuser"] == True:
                    return User.objects.create_superuser(**validated_data)
            return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
