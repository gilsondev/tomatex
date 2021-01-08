import pytest

from tomatex.core.models import Task


@pytest.fixture(scope="function")
def add_task():
    def _add_task(description):
        task = Task.objects.create(description=description)
        return task

    return _add_task
