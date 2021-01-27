import pytest

from datetime import timedelta
from django.utils import timezone

from tomatex.core.models import POMODORO_UNIT_TIMER, Pomodoro, Task


@pytest.fixture(scope="function")
def add_task():
    def _add_task(description):
        task = Task.objects.create(description=description)
        return task

    return _add_task


@pytest.fixture(scope="function")
def add_pomodoro():
    def _add_pomodoro(task, completed=True):
        started_at = timezone.now()

        if completed:
            ended_at = timezone.now() + timedelta(minutes=POMODORO_UNIT_TIMER)
        else:
            ended_at = timezone.now() + timedelta(minutes=5)

        pomodoro = Pomodoro.objects.create(
            task=task, started_at=started_at, ended_at=ended_at
        )
        return pomodoro

    return _add_pomodoro
