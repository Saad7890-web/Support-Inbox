import re

from apps.inbox.services.ai_rules.base import (
    BaseSuggestionRule,
)


class RefundRule(BaseSuggestionRule):
    patterns = [
        re.compile(r"\brefund\b", re.IGNORECASE),
        re.compile(r"\bmoney back\b", re.IGNORECASE),
        re.compile(r"\breturn\b", re.IGNORECASE),
    ]

    @classmethod
    def generate_reply(cls):
        return (
            "We're sorry for the inconvenience. "
            "We understand your concern regarding the refund request. "
            "Our support team will review your case and assist you as quickly as possible."
        )