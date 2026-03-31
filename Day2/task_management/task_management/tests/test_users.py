"""Unit tests for user endpoints."""
import json
import os
import tempfile

import pytest
from fastapi.testclient import TestClient

# point config at temp files before importing app
os.environ["USERS_FILE"] = ""
os.environ["TASKS_FILE"] = ""


def _make_client():
    """Create a fresh TestClient with isolated temp data files."""
    import importlib
    import sys

    # create temp files
    tmp_users = tempfile.NamedTemporaryFile(
        suffix=".json", delete=False, mode="w"
    )
    tmp_tasks = tempfile.NamedTemporaryFile(
        suffix=".json", delete=False, mode="w"
    )
    json.dump({"users": []}, tmp_users)
    json.dump({"tasks": []}, tmp_tasks)
    tmp_users.close()
    tmp_tasks.close()

    os.environ["USERS_FILE"] = tmp_users.name
    os.environ["TASKS_FILE"] = tmp_tasks.name

    # reload config + main to pick up new env
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


# ──────────────── Tests ────────────────

def test_register_user(client):
    resp = client.post(
        "/users/register",
        json={"username": "testuser", "email": "test@mail.com", "password": "secret123"},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["username"] == "testuser"
    assert "password" not in data


def test_register_duplicate_user(client):
    payload = {"username": "alice", "email": "alice@mail.com", "password": "secret123"}
    client.post("/users/register", json=payload)
    resp = client.post("/users/register", json=payload)
    assert resp.status_code == 409
    assert resp.json()["error"] == "DuplicateUserError"


def test_login_success(client):
    client.post(
        "/users/register",
        json={"username": "alice", "email": "alice@mail.com", "password": "secret123"},
    )
    resp = client.post("/users/login", json={"username": "alice", "password": "secret123"})
    assert resp.status_code == 200
    assert resp.json()["username"] == "alice"


def test_login_bad_password(client):
    client.post(
        "/users/register",
        json={"username": "alice", "email": "alice@mail.com", "password": "secret123"},
    )
    resp = client.post("/users/login", json={"username": "alice", "password": "wrong"})
    assert resp.status_code == 401
    assert resp.json()["error"] == "InvalidCredentialsError"


def test_list_users(client):
    client.post(
        "/users/register",
        json={"username": "alice", "email": "alice@mail.com", "password": "secret123"},
    )
    resp = client.get("/users")
    assert resp.status_code == 200
    assert len(resp.json()) == 1


def test_delete_user(client):
    r = client.post(
        "/users/register",
        json={"username": "alice", "email": "alice@mail.com", "password": "secret123"},
    )
    user_id = r.json()["id"]
    resp = client.delete(f"/users/{user_id}")
    assert resp.status_code == 200


def test_delete_nonexistent_user(client):
    resp = client.delete("/users/9999")
    assert resp.status_code == 404
    assert resp.json()["error"] == "UserNotFoundError"


def test_register_short_username(client):
    resp = client.post(
        "/users/register",
        json={"username": "ab", "email": "ab@mail.com", "password": "secret123"},
    )
    assert resp.status_code == 422


def test_register_invalid_email(client):
    resp = client.post(
        "/users/register",
        json={"username": "validuser", "email": "not-an-email", "password": "secret123"},
    )
    assert resp.status_code == 422


def test_register_short_password(client):
    resp = client.post(
        "/users/register",
        json={"username": "validuser", "email": "u@mail.com", "password": "short"},
    )
    assert resp.status_code == 422
