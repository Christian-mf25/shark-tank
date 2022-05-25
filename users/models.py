from uuid import uuid4

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, is_staff, is_superuser, **kwargs):
        now = timezone.now()
        if not email:
            raise ValueError("The given email must set")
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=True,
            last_login=now,
            date_joined=now,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **kwargs):
        kwargs.setdefault("is_staff", False)
        kwargs.setdefault("is_superuser", False)
        return self._create_user(email, password, **kwargs)

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        
        if kwargs.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")

        if kwargs.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")
        
        return self._create_user(email, password, **kwargs)


class User(AbstractUser):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=14, unique=True)
    is_inv = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    objects = UserManager()
