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
            validated_data["email"] = validated_data["email"].lower()
            validated_data["name"] = validated_data["name"].title()
            
            if not validated_phone:
                raise CustomException("phone must be (xx)xxxxx-xxxx", 400)

            if validated_data.get("is_superuser", False) and (user.is_authenticated and user.is_superuser):
                return User.objects.create_superuser(**validated_data)
            return User.objects.create_user(**validated_data)

        except IntegrityError as e:
            raise CustomException("E-mail already exists", 422)

    def update(self, instance, validated_data):
        try:
            user: user = self.context["request"].user
            
            validated_phone = None
            if validated_data.get("phone"):
                valid_phone_regex = "(\(?\d{2}\)?)?(\d{4,5}\-\d{4})"
                validated_phone = fullmatch(valid_phone_regex, validated_data["phone"])
            if validated_data.get("email", None):
                validated_data["email"] = validated_data["email"].lower()
                
            if validated_data.get("name"):
                validated_data["name"] = validated_data["name"].title()
                
            if validated_phone != None:
                raise CustomException("phone must be (xx)xxxxx-xxxx", 400)

            return super().update(instance, validated_data)

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

    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
