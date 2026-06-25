from django.db import transaction

from apps.inbox.models import (
    Message,
    SenderType,
)


class MessageService:
    @staticmethod
    @transaction.atomic
    def create_agent_reply(
        *,
        conversation,
        user,
        message_text: str,
    ):
        message = Message.objects.create(
            conversation=conversation,
            sender=user,
            sender_type=SenderType.AGENT,
            message=message_text,
        )

        conversation.last_message = message_text

        conversation.save(
            update_fields=[
                "last_message",
                "updated_at",
            ]
        )

        return message