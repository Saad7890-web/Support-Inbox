from celery import shared_task

from apps.inbox.models import (
    Conversation,
    SentimentStatus,
)


POSITIVE_WORDS = {
    "thanks",
    "thank you",
    "great",
    "awesome",
    "happy",
    "good",
    "excellent",
}

NEGATIVE_WORDS = {
    "refund",
    "angry",
    "cancel",
    "bad",
    "terrible",
    "issue",
    "problem",
}


@shared_task
def analyze_conversation_sentiment(
    conversation_id: int,
):
    try:
        conversation = (
            Conversation.objects.prefetch_related(
                "messages"
            )
            .get(id=conversation_id)
        )

    except Conversation.DoesNotExist:
        return

    messages = conversation.messages.all()

    positive_score = 0
    negative_score = 0

    for msg in messages:
        text = msg.message.lower()

        for word in POSITIVE_WORDS:
            if word in text:
                positive_score += 1

        for word in NEGATIVE_WORDS:
            if word in text:
                negative_score += 1

    if positive_score > negative_score:
        sentiment = SentimentStatus.POSITIVE

    elif negative_score > positive_score:
        sentiment = SentimentStatus.NEGATIVE

    else:
        sentiment = SentimentStatus.NEUTRAL

    conversation.sentiment = sentiment

    conversation.save(
        update_fields=[
            "sentiment",
            "updated_at",
        ]
    )