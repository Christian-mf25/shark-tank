from uuid import uuid4

from django.db import models


class Idea(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=50)
    value = models.IntegerField()
    description = models.TextField()
    amount_collected = models.IntegerField(default=0)
    finished = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(editable=False)
    is_activated = models.BooleanField(default=True)
    user= models.ForeignKey("users.User", on_delete=models.PROTECT, related_name="ideas")

