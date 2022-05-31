from uuid import uuid4

from django.db import models


class Investment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    value = models.IntegerField()
    percentage = models.FloatField()
    is_activated = models.BooleanField(default=True)
    idea = models.ForeignKey("ideas.Idea", on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
