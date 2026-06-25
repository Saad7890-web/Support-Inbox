from unittest.mock import patch
import pytest
from tests.factories.conversation_factory import (
    ConversationFactory,
)


@patch(
    "apps.inbox.views.message.analyze_conversation_sentiment.delay"
)
@pytest.mark.django_db
def test_celery_task_triggered(
    mocked_task,
    authenticated_client,
):
    conversation = ConversationFactory()

    authenticated_client.post(
        f"/api/conversations/{conversation.id}/lock/"
    )

    response = authenticated_client.post(
        f"/api/conversations/{conversation.id}/messages/send/",
        {
            "message": "refund requested"
        },
        format="json",
    )

    assert response.status_code == 201

    mocked_task.assert_called_once_with(
        conversation.id
    )