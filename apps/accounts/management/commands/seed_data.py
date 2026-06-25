from django.core.management.base import BaseCommand

from apps.accounts.models import User
from apps.inbox.models import (
    Conversation,
    Message,
    SenderType,
)


class Command(BaseCommand):
    help = "Seed initial data"

    def handle(self, *args, **kwargs):

        admin_email = "admin@test.com"

        admin, created = User.objects.get_or_create(
            email=admin_email,
            defaults={
                "full_name": "System Admin",
                "is_staff": True,
                "is_superuser": True,
            },
        )

        if created:
            admin.set_password("admin123")
            admin.save()

            self.stdout.write(
                self.style.SUCCESS(
                    "Admin user created"
                )
            )

        else:
            self.stdout.write(
                self.style.WARNING(
                    "Admin already exists"
                )
            )

        if Conversation.objects.exists():
            self.stdout.write(
                self.style.WARNING(
                    "Conversations already seeded"
                )
            )
            return

        conversations = []

        for i in range(1, 21):
            conversation = Conversation.objects.create(
                customer_name=f"Customer {i}",
                customer_email=f"customer{i}@mail.com",
                status="open",
                last_message="Initial support request",
            )

            conversations.append(conversation)

            for j in range(1, 6):
                Message.objects.create(
                    conversation=conversation,
                    sender_type=SenderType.CUSTOMER,
                    message=f"Customer message {j}",
                )

        self.stdout.write(
            self.style.SUCCESS(
                "Seed completed successfully"
            )
        )