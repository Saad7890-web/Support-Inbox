from django.urls import include, path

urlpatterns = [
    path(
        "auth/",
        include("apps.api.urls.auth"),
    ),

    path(
        "",
        include("apps.api.urls.conversations"),
    ),
    path(
        "",
        include("apps.api.urls.locks"),
    ),
    path(
        "",
        include("apps.api.urls.messages"),
    ),

    path(
        "",
        include("apps.api.urls.ai"),
    ),
]