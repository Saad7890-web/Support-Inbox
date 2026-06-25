import json

from django.core.cache import cache


LOCK_TIMEOUT_SECONDS = 300


class ConversationLockService:
    @staticmethod
    def _build_key(conversation_id: int) -> str:
        return f"conversation_lock:{conversation_id}"

    @classmethod
    def acquire_lock(cls, conversation_id, user):
        """
        Returns:
            (success, data)
        """

        key = cls._build_key(conversation_id)

        existing_lock = cache.get(key)

        # no existing lock
        if existing_lock is None:
            lock_data = {
                "user_id": user.id,
                "email": user.email,
            }

            cache.set(
                key,
                json.dumps(lock_data),
                timeout=LOCK_TIMEOUT_SECONDS,
            )

            return True, lock_data

        existing_lock = json.loads(existing_lock)

        
        if existing_lock["user_id"] == user.id:
            cache.set(
                key,
                json.dumps(existing_lock),
                timeout=LOCK_TIMEOUT_SECONDS,
            )

            return True, existing_lock

        return False, existing_lock

    @classmethod
    def get_lock(cls, conversation_id):
        key = cls._build_key(conversation_id)

        data = cache.get(key)

        if not data:
            return None

        return json.loads(data)

    @classmethod
    def release_lock(cls, conversation_id, user):
        key = cls._build_key(conversation_id)

        existing_lock = cache.get(key)

        if not existing_lock:
            return True

        existing_lock = json.loads(existing_lock)

        if existing_lock["user_id"] != user.id:
            return False

        cache.delete(key)

        return True

    @classmethod
    def is_owner(cls, conversation_id, user):
        lock = cls.get_lock(conversation_id)

        if not lock:
            return True

        return lock["user_id"] == user.id

    @classmethod
    def get_ttl(cls, conversation_id):
        key = cls._build_key(conversation_id)

        ttl = cache.ttl(key)

        if ttl is None:
            return 0

        return ttl