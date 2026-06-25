from tests.factories.conversation_factory import (
    ConversationFactory,
)

from tests.factories.user_factory import (
    UserFactory,
)

from rest_framework.test import APIClient

import pytest

@pytest.mark.django_db
def test_lock_conflict():
    conversation = ConversationFactory()

    user1 = UserFactory()
    user2 = UserFactory()

    client1 = APIClient()
    client2 = APIClient()

    token1 = client1.post(
        "/api/auth/token/",
        {
            "email": user1.email,
            "password": "password123",
        },
    ).data["access"]

    token2 = client2.post(
        "/api/auth/token/",
        {
            "email": user2.email,
            "password": "password123",
        },
    ).data["access"]

    client1.credentials(
        HTTP_AUTHORIZATION=f"Bearer {token1}"
    )

    client2.credentials(
        HTTP_AUTHORIZATION=f"Bearer {token2}"
    )

    client1.post(
        f"/api/conversations/{conversation.id}/lock/"
    )

    response = client2.post(
        f"/api/conversations/{conversation.id}/lock/"
    )

    assert response.status_code == 409