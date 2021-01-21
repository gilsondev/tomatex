import uuid

from django.db import models

POMODORO_UNIT_TIMER = 25
ONE_MINUTE = 60


class Task(models.Model):
    uid = models.UUIDField(default=uuid.uuid4)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description


class Pomodoro(models.Model):
    task = models.ForeignKey(
        "core.Task", related_name="pomodoros", on_delete=models.CASCADE
    )
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField()
    completed = models.BooleanField(default=False)

    def clean(self) -> None:
        diff = self.ended_at - self.started_at
        total_minutes = diff.seconds / ONE_MINUTE

        if total_minutes >= POMODORO_UNIT_TIMER:
            self.completed = True

    def save(self, *args, **kwargs) -> None:
        self.clean()
        return super().save(*args, **kwargs)
