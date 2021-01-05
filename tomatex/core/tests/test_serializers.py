import pytest

from tomatex.core.serializers import TaskSerializer
from tomatex.core.models import Task


def test_task_serializer():
    task = {
        "uid": "c02d91a9-7071-4927-a05d-c9d0deb357c2",
        "description": "Task Test",
        "created_at": "2020-01-01T12:00:00"
    }

    serializer = TaskSerializer(data=task)
    assert serializer.initial_data  == task
    assert 'uid' in serializer.fields
    assert 'description' in serializer.fields
    assert 'created_at' in serializer.fields


@pytest.mark.django_db
def test_task_model_serializer():
    task = Task(description="Task Model Name")
    task.save()
    serializer = TaskSerializer(task)

    assert serializer.data['uid'] == str(task.uid)
    assert serializer.data['description'] == task.description

    # TODO: Verify field and your value. Use mock in datetime now
    assert serializer.data['created_at']
