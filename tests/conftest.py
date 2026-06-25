import pytest

from rest_framework.test import APIClient

from tests.factories.user_factory import (
    UserFactory,
)


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def authenticated_client(user):
    client = APIClient()

    response = client.post(
        "/api/auth/token/",
        {
            "email": user.email,
            "password": "password123",
        },
    )

    token = response.data["access"]

    client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {token}"
    )

    return client