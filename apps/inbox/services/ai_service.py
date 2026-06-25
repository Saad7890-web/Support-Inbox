from apps.inbox.services.ai_rules.cancellation import (
    CancellationRule,
)
from apps.inbox.services.ai_rules.delay import (
    DelayRule,
)
from apps.inbox.services.ai_rules.refund import (
    RefundRule,
)
from apps.inbox.services.ai_rules.shipping import (
    ShippingRule,
)


class SuggestionEngine:
    rules = [
        RefundRule,
        ShippingRule,
        CancellationRule,
        DelayRule,
    ]

    @classmethod
    def suggest(cls, message: str) -> str:
        for rule in cls.rules:
            if rule.matches(message):
                return rule.generate_reply()

        return (
            "Thank you for reaching out. "
            "Our support team is reviewing your request and will get back to you shortly."
        )