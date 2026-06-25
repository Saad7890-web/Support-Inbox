from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.inbox.models import Conversation
from apps.inbox.services.lock_service import (
    ConversationLockService,
)


@extend_schema(tags=["Conversation Locks"])
class ConversationLockAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, conversation_id):
        conversation = get_object_or_404(
            Conversation,
            pk=conversation_id,
        )

        success, data = (
            ConversationLockService.acquire_lock(
                conversation.id,
                request.user,
            )
        )

        if not success:
            return Response(
                {
                    "detail": (
                        "Conversation locked by "
                        f"{data['email']}"
                    ),
                    "owner": data["email"],
                },
                status=status.HTTP_409_CONFLICT,
            )

        return Response(
            {
                "message": "Lock acquired",
                "owner": data["email"],
                "expires_in": 300,
            },
            status=status.HTTP_200_OK,
        )

    def get(self, request, conversation_id):
        get_object_or_404(
            Conversation,
            pk=conversation_id,
        )

        lock = ConversationLockService.get_lock(
            conversation_id
        )

        if not lock:
            return Response(
                {
                    "locked": False,
                    "owner": None,
                    "expires_in": 0,
                }
            )

        ttl = ConversationLockService.get_ttl(
            conversation_id
        )

        return Response(
            {
                "locked": True,
                "owner": lock["email"],
                "expires_in": ttl,
            }
        )

    def delete(self, request, conversation_id):
        get_object_or_404(
            Conversation,
            pk=conversation_id,
        )

        success = (
            ConversationLockService.release_lock(
                conversation_id,
                request.user,
            )
        )

        if not success:
            return Response(
                {
                    "detail":
                    "Only lock owner may release lock"
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        return Response(
            {
                "message": "Lock released"
            },
            status=status.HTTP_200_OK,
        )