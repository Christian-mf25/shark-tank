from re import fullmatch

from django.db import IntegrityError
from rest_framework import serializers

from capstone.exceptions import CustomException
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = ("uuid", "name", "username", "email", "phone", "password", "is_inv", "is_superuser", "is_staff")

        extra_kwargs = {
            "uuid": {"read_only": True},
            "password": {"write_only": True},
            "username": {"write_only": True},
            "is_inv": {"required": False, "default": False},
            "is_superuser": {"required": False, "write_only": True},
            "is_staff": {"required": False, "write_only": True},
        }

    def create(self, validated_data):
        try:

            user: User = self.context["request"].user

            valid_phone_regex = "(\(?\d{2}\)?)?(\d{4,5}\-\d{4})"
            validated_phone = fullmatch(valid_phone_regex, validated_data["phone"])

            if not validated_phone:
                raise CustomException("phone must be (xx)xxxxx-xxxx", 400)

            if validated_data.get("is_superuser", False) and (user.is_authenticated and user.is_superuser):
                return User.objects.create_superuser(**validated_data)
            return User.objects.create_user(**validated_data)

        except IntegrityError as e:
            raise CustomException("E-mail already exists", 422)


class UserInvestmetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = (
            "name",
            "email",
        )


class LoginSerializer(serializers.Serializer):
    
    def validate(self, attrs):
        attrs["name"] = attrs["name"].title()
        attrs["email"] = attrs["email"].lower()

        return super().validate(attrs)

    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
