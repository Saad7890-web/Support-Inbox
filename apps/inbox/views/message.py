from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema

from rest_framework import status
from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.inbox.models import Conversation

from apps.inbox.serializers.message import (
    CreateMessageSerializer,
)

from apps.inbox.services.lock_service import (
    ConversationLockService,
)

from apps.inbox.services.message_service import (
    MessageService,
)

from apps.inbox.tasks import (
    analyze_conversation_sentiment,
)


@extend_schema(
    tags=["Messages"],
    request=CreateMessageSerializer,
)
class SendMessageAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, conversation_id):
        conversation = get_object_or_404(
            Conversation,
            pk=conversation_id,
        )

        if not ConversationLockService.is_owner(
            conversation_id,
            request.user,
        ):
            lock = (
                ConversationLockService.get_lock(
                    conversation_id
                )
            )

            return Response(
                {
                    "detail": (
                        "Conversation locked by "
                        f"{lock['email']}"
                    )
                },
                status=status.HTTP_409_CONFLICT,
            )

        serializer = CreateMessageSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        message = (
            MessageService.create_agent_reply(
                conversation=conversation,
                user=request.user,
                message_text=serializer.validated_data[
                    "message"
                ],
            )
        )

        
        analyze_conversation_sentiment.delay(
            conversation.id
        )

        return Response(
            {
                "id": message.id,
                "message": message.message,
                "status": "queued_for_analysis",
            },
            status=status.HTTP_201_CREATED,
        )