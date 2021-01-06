import pytest
from django.urls import reverse
from rest_framework import status

task_new_data = {
    "description": "Task Test"
}

@pytest.mark.django_db
def test_request_create_task(client):
    resp = client.post(reverse('tasks_resource'), task_new_data,
                       content_type="application/json")

    assert resp.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_response_create_task(client):
    resp = client.post(reverse('tasks_resource'), task_new_data,
                       content_type="application/json")

    assert 'uid' in resp.data
    assert resp.data['description'] == "Task Test"
    assert 'created_at' in resp.data


@pytest.mark.django_db
def test_response_task_not_return_id_field(client):
    resp = client.post(reverse('tasks_resource'), task_new_data,
                       content_type="application/json")

    assert 'id' not in resp.data


def test_dont_create_invalid_task(client):
    resp = client.post(reverse('tasks_resource'), {
        "description": None
    }, content_type="application/json")

    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert 'description' in resp.data


@pytest.mark.django_db
def test_list_task(client, add_task):
    add_task(description="Task #1")
    add_task(description="Task #2")

    resp = client.get(reverse('tasks_resource'))

    assert resp.status_code == status.HTTP_200_OK
    assert len(resp.data) == 2


@pytest.mark.django_db
def test_fetch_task_by_uid(client, add_task):
    task = add_task(description="Task #1")
    resp = client.get(reverse('tasks_detail_resource',
                      kwargs={'uid': task.uid}))

    assert resp.status_code == status.HTTP_200_OK
    assert resp.data['uid'] == str(task.uid)
    assert resp.data['description'] == task.description
    assert 'created_at' in resp.data
