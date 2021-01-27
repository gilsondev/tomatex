import pytest
import json

from tomatex.core.models import Task
from tomatex.core.serializers import (
    TaskPomodoroSerializer,
    TaskSerializer,
    TaskPomodorosSerializer,
)


def test_task_serializer():
    task = {
        "uid": "c02d91a9-7071-4927-a05d-c9d0deb357c2",
        "description": "Task Test",
        "created_at": "2020-01-01T12:00:00",
    }

    serializer = TaskSerializer(data=task)
    assert serializer.initial_data == task
    assert "uid" in serializer.fields
    assert "description" in serializer.fields
    assert "created_at" in serializer.fields


@pytest.mark.django_db
def test_task_model_serializer():
    task = Task(description="Task Model Name")
    task.save()
    serializer = TaskSerializer(task)

    assert serializer.data["uid"] == str(task.uid)
    assert serializer.data["description"] == task.description

    # TODO: Verify field and your value. Use mock in datetime now
    assert serializer.data["created_at"]


@pytest.mark.django_db
def test_pomodoro_serializer(add_task):
    task = add_task(description="Task Pomodoro")
    pomodoro = {
        "started_at": "2020-01-01T12:00:00Z",
        "ended_at": "2020-01-01T12:25:00Z",
    }

    serializer = TaskPomodoroSerializer(task=task, data=pomodoro)

    assert serializer.is_valid()
    assert serializer.data["started_at"] == pomodoro["started_at"]
    assert serializer.data["ended_at"] == pomodoro["ended_at"]
    assert "started_at" in serializer.fields
    assert "ended_at" in serializer.fields
    assert "completed" in serializer.fields


@pytest.mark.django_db
def test_create_pomodoro_serializer(add_task):
    task = add_task(description="Task Pomodoro")
    pomodoro = {
        "started_at": "2020-01-01T12:00:00Z",
        "ended_at": "2020-01-01T12:25:00Z",
    }

    serializer = TaskPomodoroSerializer(task=task, data=pomodoro)

    assert serializer.is_valid()

    pomodoro = serializer.save()
    assert pomodoro.id
    assert pomodoro.task.id == task.id
    assert pomodoro.completed


@pytest.mark.django_db
def test_list_pomodoro_serializer(add_task, add_pomodoro):
    task = add_task(description="Task Pomodoro")
    add_pomodoro(task=task, completed=True)

    data = {
        "uid": str(task.uid),
        "description": task.description,
        "pomodoros": {"completed": 1, "incompleted": 0},
    }

    serializer = TaskPomodorosSerializer(task)

    assert json.dumps(serializer.data) == json.dumps(data)
