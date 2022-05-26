from rest_framework import serializers
from ideas.serializers import IdeaSerializer

from users.serializers import UserSerializer


class InvestmentSerializer(serializers.Serializer):
    id=serializers.UUIDField(read_only=True)
    value=serializers.IntegerField()
    percentage=serializers.FloatField(read_only=True)
    idea_id = serializers.UUIDField(write_only=True)
    user=UserSerializer(read_only=True)
    idea=IdeaSerializer(read_only=True)
