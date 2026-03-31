"""Unit tests for task endpoints."""
import json
import os
import tempfile

import pytest
from fastapi.testclient import TestClient


def _make_client():
    import sys

    tmp_users = tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w")
    tmp_tasks = tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w")
    json.dump({"users": []}, tmp_users)
    json.dump({"tasks": []}, tmp_tasks)
    tmp_users.close()
    tmp_tasks.close()

    os.environ["USERS_FILE"] = tmp_users.name
    os.environ["TASKS_FILE"] = tmp_tasks.name

    for mod in ["config", "main"]:
        if mod in sys.modules:
            del sys.modules[mod]

    from main import app  # noqa: PLC0415
    client = TestClient(app, raise_server_exceptions=False)
    return client, tmp_users.name, tmp_tasks.name


@pytest.fixture()
def client():
    c, u, t = _make_client()
    yield c
    os.unlink(u)
    os.unlink(t)


TASK_PAYLOAD = {
    "title": "Fix login bug",
    "description": "Users cannot log in on mobile",
    "priority": "high",
    "status": "pending",
    "owner": "alice",
}


def test_create_task(client):
    resp = client.post("/tasks", json=TASK_PAYLOAD)
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "Fix login bug"
    assert data["owner"] == "alice"
    assert "id" in data


def test_list_tasks(client):
    client.post("/tasks", json=TASK_PAYLOAD)
    resp = client.get("/tasks")
    assert resp.status_code == 200
    assert len(resp.json()) == 1


def test_filter_by_status(client):
    client.post("/tasks", json=TASK_PAYLOAD)
    client.post("/tasks", json={**TASK_PAYLOAD, "title": "Another task", "status": "completed"})
    resp = client.get("/tasks?status=pending")
    assert resp.status_code == 200
    assert all(t["status"] == "pending" for t in resp.json())


def test_filter_by_priority(client):
    client.post("/tasks", json=TASK_PAYLOAD)
    client.post("/tasks", json={**TASK_PAYLOAD, "title": "Low prio task", "priority": "low"})
    resp = client.get("/tasks?priority=high")
    assert all(t["priority"] == "high" for t in resp.json())


def test_filter_by_owner(client):
    client.post("/tasks", json=TASK_PAYLOAD)
    client.post("/tasks", json={**TASK_PAYLOAD, "title": "Bob task", "owner": "bob"})
    resp = client.get("/tasks?owner=alice")
    assert all(t["owner"] == "alice" for t in resp.json())


def test_pagination(client):
    for i in range(5):
        client.post("/tasks", json={**TASK_PAYLOAD, "title": f"Task {i}"})
    resp = client.get("/tasks?page=1&limit=2")
    assert len(resp.json()) == 2
    resp2 = client.get("/tasks?page=3&limit=2")
    assert len(resp2.json()) == 1


def test_pagination_beyond_data_returns_empty(client):
    client.post("/tasks", json=TASK_PAYLOAD)
    resp = client.get("/tasks?page=999&limit=10")
    assert resp.status_code == 200
    assert resp.json() == []


def test_get_task_by_id(client):
    created = client.post("/tasks", json=TASK_PAYLOAD).json()
    resp = client.get(f"/tasks/{created['id']}")
    assert resp.status_code == 200
    assert resp.json()["id"] == created["id"]


def test_get_task_not_found(client):
    resp = client.get("/tasks/9999")
    assert resp.status_code == 404
    assert resp.json()["error"] == "TaskNotFoundError"


def test_full_update_task(client):
    created = client.post("/tasks", json=TASK_PAYLOAD).json()
    update = {**TASK_PAYLOAD, "title": "Updated title", "status": "in_progress"}
    resp = client.put(f"/tasks/{created['id']}", json=update)
    assert resp.status_code == 200
    assert resp.json()["title"] == "Updated title"
    assert resp.json()["status"] == "in_progress"


def test_partial_update_task(client):
    created = client.post("/tasks", json=TASK_PAYLOAD).json()
    resp = client.patch(f"/tasks/{created['id']}", json={"status": "completed"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "completed"
    assert resp.json()["title"] == TASK_PAYLOAD["title"]  # unchanged


def test_delete_task(client):
    created = client.post("/tasks", json=TASK_PAYLOAD).json()
    resp = client.delete(f"/tasks/{created['id']}")
    assert resp.status_code == 200
    assert client.get(f"/tasks/{created['id']}").status_code == 404


def test_delete_nonexistent_task(client):
    resp = client.delete("/tasks/9999")
    assert resp.status_code == 404
    assert resp.json()["error"] == "TaskNotFoundError"


def test_create_task_blank_title(client):
    resp = client.post("/tasks", json={**TASK_PAYLOAD, "title": "   "})
    assert resp.status_code == 422


def test_create_task_invalid_priority(client):
    resp = client.post("/tasks", json={**TASK_PAYLOAD, "priority": "ultra"})
    assert resp.status_code == 422


def test_create_task_invalid_status(client):
    resp = client.post("/tasks", json={**TASK_PAYLOAD, "status": "done"})
    assert resp.status_code == 422
