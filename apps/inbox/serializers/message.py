from rest_framework import serializers


class CreateMessageSerializer(serializers.Serializer):
    message = serializers.CharField(
        max_length=5000
    )