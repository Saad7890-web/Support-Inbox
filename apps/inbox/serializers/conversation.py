from rest_framework import serializers

from apps.inbox.models import (
    Conversation,
    Message,
)


class ConversationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation

        fields = (
            "id",
            "customer_name",
            "last_message",
            "status",
            "created_at",
        )


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()

    class Meta:
        model = Message

        fields = (
            "id",
            "sender",
            "message",
            "created_at",
        )

    def get_sender(self, obj):
        if obj.sender:
            return obj.sender.email

        return obj.sender_type