import re

from apps.inbox.services.ai_rules.base import (
    BaseSuggestionRule,
)


class DelayRule(BaseSuggestionRule):
    patterns = [
        re.compile(r"\blate\b", re.IGNORECASE),
        re.compile(r"\bdelay\b", re.IGNORECASE),
        re.compile(r"\bdelayed\b", re.IGNORECASE),
    ]

    @classmethod
    def generate_reply(cls):
        return (
            "We apologize for the delay. "
            "Our team is currently investigating the issue and will provide an update shortly."
        )