from apps.inbox.services.lock_service import (
    ConversationLockService,
)

from tests.factories.user_factory import (
    UserFactory,
)


def test_acquire_lock():
    user = UserFactory()

    success, data = (
        ConversationLockService.acquire_lock(
            1,
            user,
        )
    )

    assert success is True
    assert data["user_id"] == user.id


def test_lock_owner_check():
    user = UserFactory()

    ConversationLockService.acquire_lock(
        1,
        user,
    )

    assert (
        ConversationLockService.is_owner(
            1,
            user,
        )
        is True
    )


def test_lock_ttl_exists():
    user = UserFactory()

    ConversationLockService.acquire_lock(
        1,
        user,
    )

    ttl = (
        ConversationLockService.get_ttl(1)
    )

    assert ttl > 0