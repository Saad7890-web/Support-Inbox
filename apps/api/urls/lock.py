from django.urls import path

from apps.inbox.views.lock import (
    ConversationLockAPIView,
)

urlpatterns = [
    path(
        "conversations/<int:conversation_id>/lock/",
        ConversationLockAPIView.as_view(),
        name="conversation-lock",
    ),
]