import django_filters

from apps.inbox.models import Conversation


class ConversationFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(
        field_name="status",
        lookup_expr="exact",
    )

    class Meta:
        model = Conversation
        fields = ["status"]