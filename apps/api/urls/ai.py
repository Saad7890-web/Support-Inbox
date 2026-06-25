from django.urls import path

from apps.inbox.views.ai import (
    SuggestReplyAPIView,
)

urlpatterns = [
    path(
        "conversations/<int:conversation_id>/suggest-reply/",
        SuggestReplyAPIView.as_view(),
        name="suggest-reply",
    ),
]