from django.urls import path

from apps.api.views.auth import (
    LoginView,
    RefreshTokenView,
)

urlpatterns = [
    path(
        "token/",
        LoginView.as_view(),
        name="token_obtain_pair",
    ),

    path(
        "token/refresh/",
        RefreshTokenView.as_view(),
        name="token_refresh",
    ),
]