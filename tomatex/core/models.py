import uuid

from django.db import models


class Task(models.Model):
    uid = models.UUIDField(default=uuid.uuid4)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description
