from django.db import models


class PomodoroManager(models.Manager):
    def total_completed(self):
        return super().get_queryset().filter(completed=True).count()

    def total_incompleted(self):
        return super().get_queryset().filter(completed=False).count()
