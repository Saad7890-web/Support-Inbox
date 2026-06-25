import factory

from apps.inbox.models import (
    Conversation,
    ConversationStatus,
)


class ConversationFactory(
    factory.django.DjangoModelFactory
):
    class Meta:
        model = Conversation

    customer_name = factory.Faker("name")

    last_message = factory.Faker("sentence")

    status = ConversationStatus.OPEN