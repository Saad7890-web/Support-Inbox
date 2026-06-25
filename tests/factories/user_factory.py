import factory

from apps.accounts.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(
        lambda n: f"user{n}@test.com"
    )

    full_name = factory.Faker("name")

    password = factory.PostGenerationMethodCall(
        "set_password",
        "password123",
    )