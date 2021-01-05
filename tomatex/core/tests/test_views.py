import pytest

@pytest.mark.django_db
def test_request_create_task(client):
    resp = client.post('/api/tasks', {
        "description": "Task Test"
    }, content_type="application/json")

    assert resp.status_code == 201


@pytest.mark.django_db
def test_response_create_task(client):
    resp = client.post('/api/tasks', {
        "description": "Task Test"
    }, content_type="application/json")

    assert 'uid' in resp.data
    assert resp.data['description'] == "Task Test"
    assert 'created_at' in resp.data


@pytest.mark.django_db
def test_response_task_not_return_id_field(client):
    resp = client.post('/api/tasks', {
        "description": "Task Test"
    }, content_type="application/json")

    assert 'id' not in resp.data


def test_dont_create_invalid_task(client):
    resp = client.post('/api/tasks', {
        "description": None
    }, content_type="application/json")

    assert resp.status_code == 400
    assert 'description' in resp.data