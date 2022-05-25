from capstone.exceptions import CustomException
from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("uuid", "name", "email", "password", "phone", "is_inv", "is_superuser")
        extra_kwargs = {"uuid": {"read_only": True}, "password": {"write_only": True}}

    def validate(self, attrs):
        attrs["name"] = attrs["name"].title()
        attrs["email"] = attrs["email"].lower()
        return super().validate(attrs)

    def create(self, validated_data):
        user: User = self.context["request"].user
        if validated_data.get("is_superuser", False) and (user.is_authenticated and user.is_superuser):
            return User.objects.create_superuser(**validated_data)
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
