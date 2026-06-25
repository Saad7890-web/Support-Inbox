from asgiref.sync import async_to_sync

from channels.layers import (
    get_channel_layer,
)


class BroadcastService:
    @staticmethod
    def broadcast_message(message):
        channel_layer = get_channel_layer()

        async_to_sync(
            channel_layer.group_send
        )(
            f"conversation_{message.conversation.id}",
            {
                "type": "new_message",

                "message": {
                    "id": message.id,
                    "conversation_id":
                        message.conversation.id,

                    "sender":
                        (
                            message.sender.email
                            if message.sender
                            else message.sender_type
                        ),

                    "message":
                        message.message,

                    "created_at":
                        message.created_at.isoformat(),
                },
            },
        )