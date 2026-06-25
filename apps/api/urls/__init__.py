from django.urls import include, path

urlpatterns = [
    path(
        "auth/",
        include("apps.api.urls.auth"),
    ),
]