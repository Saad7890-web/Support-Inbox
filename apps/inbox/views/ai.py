from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema

from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.inbox.models import Conversation

from apps.inbox.serializers.ai import (
    SuggestReplySerializer,
)

from apps.inbox.services.ai_service import (
    SuggestionEngine,
)


@extend_schema(
    tags=["AI Suggestions"],
    request=SuggestReplySerializer,
)
class SuggestReplyAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, conversation_id):
        get_object_or_404(
            Conversation,
            pk=conversation_id,
        )

        serializer = SuggestReplySerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        suggestion = SuggestionEngine.suggest(
            serializer.validated_data["message"]
        )

        return Response(
            {
                "suggestion": suggestion
            }
        )