from tests.factories.conversation_factory import (
    ConversationFactory,
)

import pytest

@pytest.mark.django_db
def test_authentication_required(
    api_client,
):
    response = api_client.get(
        "/api/conversations/"
    )

    assert response.status_code == 401

@pytest.mark.django_db
def test_conversation_listing(
    authenticated_client,
):
    ConversationFactory.create_batch(15)

    response = authenticated_client.get(
        "/api/conversations/"
    )

    assert response.status_code == 200
    assert "results" in response.data

@pytest.mark.django_db
def test_search_filter(
    authenticated_client,
):
    ConversationFactory(
        customer_name="John Doe"
    )

    response = authenticated_client.get(
        "/api/conversations/?search=John"
    )

    assert response.status_code == 200

    assert response.data["count"] >= 1