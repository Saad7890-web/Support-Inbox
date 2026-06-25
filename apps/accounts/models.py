from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.db import models

from apps.accounts.managers import UserManager
from apps.common.models import TimeStampedModel


class User(TimeStampedModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True,
        db_index=True,
    )

    full_name = models.CharField(
        max_length=255,
    )

    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []

    class Meta:
        db_table = "users"
        ordering = ["-created_at"]

    def __str__(self):
        return self.email