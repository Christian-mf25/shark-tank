from rest_framework import serializers
# from users.serializers import UserSerializer

class IdeaSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only= True)
    name = serializers.CharField()
    description = serializers.CharField()
    value = serializers.IntegerField()
    amount_collected = serializers.IntegerField(read_only=True)
    finished = serializers.BooleanField(read_only=True)
    createt_at = serializers.DateTimeField(read_only=True, format="%d/%m/%Y")
    deadline = serializers.DateTimeField(read_only= True, format="%d/%m/%Y")
    # user_id = UserSerializer(read_only=True)

