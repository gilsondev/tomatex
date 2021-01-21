import pytest
from django.urls import reverse
from rest_framework import status

from tomatex.core.serializers import TaskPomodoroSerializer
from tomatex.core.models import Task

task_new_data = {"description": "Task Test"}


@pytest.mark.django_db
def test_request_create_task(client):
    resp = client.post(
        reverse("tasks_resource"), task_new_data, content_type="application/json"
    )

    assert resp.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_response_create_task(client):
    resp = client.post(
        reverse("tasks_resource"), task_new_data, content_type="application/json"
    )

    assert "uid" in resp.data
    assert resp.data["description"] == "Task Test"
    assert "created_at" in resp.data


@pytest.mark.django_db
def test_response_task_not_return_id_field(client):
    resp = client.post(
        reverse("tasks_resource"), task_new_data, content_type="application/json"
    )

    assert "id" not in resp.data


def test_dont_create_invalid_task(client):
    resp = client.post(
        reverse("tasks_resource"),
        {"description": None},
        content_type="application/json",
    )

    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert "description" in resp.data


@pytest.mark.django_db
def test_list_task(client, add_task):
    add_task(description="Task #1")
    add_task(description="Task #2")

    resp = client.get(reverse("tasks_resource"))

    assert resp.status_code == status.HTTP_200_OK
    assert len(resp.data) == 2


@pytest.mark.django_db
def test_fetch_task_by_uid(client, add_task):
    task = add_task(description="Task #1")
    resp = client.get(reverse("tasks_detail_resource", kwargs={"uid": task.uid}))

    assert resp.status_code == status.HTTP_200_OK
    assert resp.data["uid"] == str(task.uid)
    assert resp.data["description"] == task.description
    assert "created_at" in resp.data


@pytest.mark.django_db
def test_request_task_not_found(client):
    uid = "c02d91a9-7071-4927-a05d-c9d0deb357c2"
    resp = client.get(reverse("tasks_detail_resource", kwargs={"uid": uid}))

    assert resp.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_update_task(client, add_task):
    task = add_task(description="Task #1")

    resp = client.put(
        reverse("tasks_detail_resource", kwargs={"uid": task.uid}),
        {"description": "Task Updated"},
        content_type="application/json",
    )

    assert resp.status_code == status.HTTP_204_NO_CONTENT

    updated_task = Task.objects.get(uid=task.uid)
    assert updated_task.description == "Task Updated"


@pytest.mark.django_db
def test_not_update_invalid_task(client):
    uid = "c02d91a9-7071-4927-a05d-c9d0deb357c2"
    resp = client.put(
        reverse("tasks_detail_resource", kwargs={"uid": uid}),
        {"description": "Task Updated"},
        content_type="application/json",
    )

    assert resp.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_remove_task(client, add_task):
    task = add_task(description="Task #1")

    resp = client.delete(reverse("tasks_detail_resource", kwargs={"uid": task.uid}))

    assert resp.status_code == 204
    assert not Task.objects.exists()


def test_request_task_pomodoros(client):
    import uuid

    uid = uuid.uuid4()
    resp = client.get(f"/api/tasks/{uid}/pomodoros")

    assert resp.status_code == 200


def test_response_task_pomodoros(client):
    import uuid

    uid = uuid.uuid4()
    resp = client.get(f"/api/tasks/{uid}/pomodoros")

    assert len(resp.data) > 0
    assert "uid" in resp.data[0]
    assert resp.data[0]["description"] == "Task Name"
    assert len(resp.data[0]["completed"]) > 0
    assert resp.data[0]["completed"][0]["started_at"] == "2020-01-01T12:00:00"
    assert resp.data[0]["completed"][0]["ended_at"] == "2020-01-01T12:25:00"
    assert resp.data[0]["completed"][0]["duration"] == "25:00"


@pytest.mark.django_db
def test_create_new_pomodoro(client, add_task):
    task = add_task(description="Task #1")

    data = {"started_at": "2020-01-01T12:00:00", "ended_at": "2020-01-01T12:25:00"}
    resp = client.post(
        f"/api/tasks/{task.uid}/pomodoros",
        data,
        content_type="application/json",
    )

    assert resp.status_code == 201


@pytest.mark.django_db
def test_response_create_new_pomodoro(client, add_task):
    task = add_task(description="Task #1")

    data = {"started_at": "2020-01-01T12:00:00Z", "ended_at": "2020-01-01T12:25:00Z"}
    resp = client.post(
        f"/api/tasks/{task.uid}/pomodoros", data, content_type="application/json"
    )

    task = Task.objects.get(uid=task.uid)
    pomodoro = task.pomodoros.first()
    serializer = TaskPomodoroSerializer(task=task, instance=pomodoro)

    assert resp.data["started_at"] == serializer.data["started_at"]
    assert resp.data["ended_at"] == serializer.data["ended_at"]
    assert resp.data["completed"]
