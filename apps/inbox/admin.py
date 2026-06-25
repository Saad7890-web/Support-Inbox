from django.contrib import admin

from apps.inbox.models import Conversation, Message


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer_name",
        "status",
        "sentiment",
        "created_at",
    )

    search_fields = (
        "customer_name",
        "customer_email",
    )

    list_filter = (
        "status",
        "sentiment",
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "conversation",
        "sender_type",
        "created_at",
    )

    search_fields = ("message",)

    list_filter = ("sender_type",)