import factory

from apps.inbox.models import (
    Message,
    SenderType,
)

from tests.factories.conversation_factory import (
    ConversationFactory,
)

from tests.factories.user_factory import (
    UserFactory,
)


class MessageFactory(
    factory.django.DjangoModelFactory
):
    class Meta:
        model = Message

    conversation = factory.SubFactory(
        ConversationFactory
    )

    sender = factory.SubFactory(UserFactory)

    sender_type = SenderType.AGENT

    message = factory.Faker("sentence")