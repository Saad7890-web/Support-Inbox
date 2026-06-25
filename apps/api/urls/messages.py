from django.urls import path

from apps.inbox.views.message import (
    SendMessageAPIView,
)

urlpatterns = [
    path(
        "conversations/<int:conversation_id>/messages/send/",
        SendMessageAPIView.as_view(),
        name="send-message",
    ),
]