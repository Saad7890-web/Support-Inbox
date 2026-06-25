import re

from apps.inbox.services.ai_rules.base import (
    BaseSuggestionRule,
)


class ShippingRule(BaseSuggestionRule):
    patterns = [
        re.compile(r"\bshipping\b", re.IGNORECASE),
        re.compile(r"\bdelivery\b", re.IGNORECASE),
        re.compile(r"\btracking\b", re.IGNORECASE),
    ]

    @classmethod
    def generate_reply(cls):
        return (
            "Thank you for contacting us. "
            "Please share your order number so we can check the current shipping status for you."
        )