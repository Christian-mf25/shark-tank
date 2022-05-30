from rest_framework import serializers

from users.serializers import UserInvestmetSerializer


class IdeaSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField()
    value = serializers.IntegerField()
    amount_collected = serializers.IntegerField(read_only=True)
    finished = serializers.BooleanField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True, format="%d/%m/%Y")
    deadline = serializers.DateTimeField(read_only=True, format="%d/%m/%Y")
    is_activated = serializers.BooleanField(read_only=True)
    user = UserInvestmetSerializer(read_only=True)


class IdeaUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    # value = serializers.IntegerField(required=False)
    is_activated = serializers.BooleanField(required=False)


class IdeaInvestmentsSerializer(serializers.Serializer):
    user = UserInvestmetSerializer()
    value = serializers.IntegerField()
