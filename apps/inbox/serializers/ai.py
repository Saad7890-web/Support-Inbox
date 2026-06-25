from rest_framework import serializers


class SuggestReplySerializer(serializers.Serializer):
    message = serializers.CharField(
        max_length=5000
    )