from rest_framework import serializers


class LockStatusSerializer(serializers.Serializer):
    locked = serializers.BooleanField()
    owner = serializers.CharField(
        allow_null=True
    )
    expires_in = serializers.IntegerField()