from uuid import uuid4

from django.db import models


class Investment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    value = models.IntegerField()
    percentage = models.FloatField()
    idea = models.ForeignKey("ideas.Idea", on_delete=models.PROTECT)
    user = models.ForeignKey("users.User", on_delete=models.PROTECT)
