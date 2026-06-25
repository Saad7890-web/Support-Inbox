from django.conf import settings
from django.db import models

from apps.common.models import TimeStampedModel


class ConversationStatus(models.TextChoices):
    OPEN = "open", "Open"
    PENDING = "pending", "Pending"
    RESOLVED = "resolved", "Resolved"
    CLOSED = "closed", "Closed"


class SentimentStatus(models.TextChoices):
    UNKNOWN = "unknown", "Unknown"
    POSITIVE = "positive", "Positive"
    NEUTRAL = "neutral", "Neutral"
    NEGATIVE = "negative", "Negative"


class Conversation(TimeStampedModel):
    customer_name = models.CharField(
        max_length=255,
        db_index=True,
    )

    customer_email = models.EmailField(
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=ConversationStatus.choices,
        default=ConversationStatus.OPEN,
        db_index=True,
    )

    sentiment = models.CharField(
        max_length=20,
        choices=SentimentStatus.choices,
        default=SentimentStatus.UNKNOWN,
        db_index=True,
    )

    last_message = models.TextField(
        blank=True,
    )

    class Meta:
        db_table = "conversations"

        ordering = ["-created_at"]

        indexes = [
            models.Index(
                fields=["customer_name"],
                name="conv_customer_idx",
            ),

            models.Index(
                fields=["status"],
                name="conv_status_idx",
            ),

            models.Index(
                fields=["created_at"],
                name="conv_created_idx",
            ),
        ]

    def __str__(self):
        return f"{self.customer_name} ({self.status})"

class SenderType(models.TextChoices):
    CUSTOMER = "customer", "Customer"
    AGENT = "agent", "Agent"
    SYSTEM = "system", "System"


class Message(TimeStampedModel):
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages",
    )

    sender_type = models.CharField(
        max_length=20,
        choices=SenderType.choices,
        db_index=True,
    )

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="sent_messages",
    )

    message = models.TextField()

    class Meta:
        db_table = "messages"

        ordering = ["created_at"]

        indexes = [
            models.Index(
                fields=["conversation", "created_at"],
                name="msg_conv_created_idx",
            ),
        ]

    def __str__(self):
        return f"{self.sender_type} - {self.id}"