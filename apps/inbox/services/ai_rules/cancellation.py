import re

from apps.inbox.services.ai_rules.base import (
    BaseSuggestionRule,
)


class CancellationRule(BaseSuggestionRule):
    patterns = [
        re.compile(r"\bcancel\b", re.IGNORECASE),
        re.compile(r"\bcancellation\b", re.IGNORECASE),
    ]

    @classmethod
    def generate_reply(cls):
        return (
            "We understand you'd like to cancel your order. "
            "Please provide your order details and we'll assist you with the cancellation process."
        )