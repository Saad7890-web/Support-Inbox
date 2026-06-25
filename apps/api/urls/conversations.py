from django.urls import path

from apps.inbox.views.conversation import (
    ConversationListAPIView,
    ConversationMessageListAPIView,
)

urlpatterns = [
    path(
        "conversations/",
        ConversationListAPIView.as_view(),
        name="conversation-list",
    ),

    path(
        "conversations/<int:conversation_id>/messages/",
        ConversationMessageListAPIView.as_view(),
        name="conversation-messages",
    ),
]