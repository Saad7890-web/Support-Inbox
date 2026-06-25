from tests.factories.conversation_factory import (
    ConversationFactory,
)

from tests.factories.message_factory import (
    MessageFactory,
)

import pytest

@pytest.mark.django_db
def test_conversation_total_messages():
    conversation = ConversationFactory()

    MessageFactory.create_batch(
        3,
        conversation=conversation,
    )

    assert (
        conversation.total_messages == 3
    )