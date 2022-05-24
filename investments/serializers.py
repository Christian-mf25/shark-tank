from rest_framework import serializers


class InvestmentSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    value = serializers.IntegerField()
    percentage = serializers.IntegerField(read_only=True)
    idea_id = serializers.UUIDField(read_only=True)
    user_id = serializers.UUIDField(read_only=True)
