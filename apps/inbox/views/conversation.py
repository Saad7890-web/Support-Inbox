from django.shortcuts import get_object_or_404

from django_filters.rest_framework import (
    DjangoFilterBackend,
)

from drf_spectacular.utils import (
    OpenApiParameter,
    extend_schema,
)

from rest_framework import filters, generics
from rest_framework.permissions import IsAuthenticated

from apps.api.pagination import DefaultPagination

from apps.inbox.filters.conversation import (
    ConversationFilter,
)

from apps.inbox.models import Conversation

from apps.inbox.selectors.conversation_selector import (
    get_conversation_messages,
    get_conversations,
)

from apps.inbox.serializers.conversation import (
    ConversationListSerializer,
    MessageSerializer,
)


@extend_schema(
    tags=["Conversations"],
    parameters=[
        OpenApiParameter(
            name="search",
            type=str,
            location=OpenApiParameter.QUERY,
            description="Search by customer name",
        ),
        OpenApiParameter(
            name="status",
            type=str,
            location=OpenApiParameter.QUERY,
            description="Conversation status",
        ),
    ],
)
class ConversationListAPIView(generics.ListAPIView):
    serializer_class = ConversationListSerializer

    permission_classes = [IsAuthenticated]

    pagination_class = DefaultPagination

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_class = ConversationFilter

    search_fields = ["customer_name"]

    ordering_fields = [
        "created_at",
        "customer_name",
    ]

    ordering = ["-created_at"]

    def get_queryset(self):
        return get_conversations()


@extend_schema(tags=["Messages"])
class ConversationMessageListAPIView(
    generics.ListAPIView
):
    serializer_class = MessageSerializer

    permission_classes = [IsAuthenticated]

    pagination_class = None

    def get_queryset(self):
        conversation = get_object_or_404(
            Conversation,
            pk=self.kwargs["conversation_id"],
        )

        return get_conversation_messages(
            conversation.id
        )