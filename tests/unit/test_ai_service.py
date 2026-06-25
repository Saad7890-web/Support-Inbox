from apps.inbox.services.ai_service import (
    SuggestionEngine,
)


def test_refund_rule_matches():
    response = SuggestionEngine.suggest(
        "Customer wants refund"
    )

    assert "refund" in response.lower()


def test_shipping_rule_matches():
    response = SuggestionEngine.suggest(
        "delivery status"
    )

    assert "order number" in response.lower()


def test_default_rule():
    response = SuggestionEngine.suggest(
        "hello"
    )

    assert "support team" in response.lower()