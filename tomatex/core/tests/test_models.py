import pytest

from tomatex.core.models import Task


@pytest.mark.django_db
def test_task_model():
    task = Task(description="Task Name")
    task.save()

    assert task.id
    assert task.uid
    assert task.description == "Task Name"
    assert task.created_at
    assert str(task) == task.description
