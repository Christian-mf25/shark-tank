from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=14, unique=True)
    is_inv = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
