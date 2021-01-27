import pytest

from datetime import timedelta
from django.utils import timezone

from tomatex.core.models import Task, Pomodoro


@pytest.mark.django_db
def test_task_model():
    task = Task(description="Task Name")
    task.save()

    assert task.id
    assert task.uid
    assert task.description == "Task Name"
    assert task.created_at
    assert str(task) == task.description


@pytest.mark.django_db
def test_task_pomodoro_model(add_task, add_pomodoro):
    task = add_task(description="Task Pomodoro")
    pomodoro = add_pomodoro(task=task, completed=True)

    assert pomodoro.id
    assert pomodoro.task.id == task.id
    assert pomodoro.completed


@pytest.mark.django_db
def test_count_completed_pomodoros(add_task, add_pomodoro):
    task = add_task(description="Task Pomodoro")
    add_pomodoro(task=task, completed=True)

    assert task.pomodoros.total_completed() == 1


@pytest.mark.django_db
def test_count_incompleted_pomodoros(add_task, add_pomodoro):
    task = add_task(description="Task Pomodoro")
    add_pomodoro(task=task, completed=False)

    assert task.pomodoros.total_incompleted() == 1
