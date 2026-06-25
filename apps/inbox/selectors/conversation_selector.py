from django.db.models import QuerySet

from apps.inbox.models import Conversation, Message


def get_conversations() -> QuerySet[Conversation]:
    return Conversation.objects.all()


def get_conversation_messages(
    conversation_id: int,
) -> QuerySet[Message]:
    return (
        Message.objects.select_related("sender")
        .filter(conversation_id=conversation_id)
        .order_by("created_at")
    )