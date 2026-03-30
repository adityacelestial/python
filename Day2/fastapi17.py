
# Q17. API Testing with pytest 

# Topics: Testing, pytest, TestClient 

# Problem Statement: 

# Write automated tests for the Task API using pytest and FastAPI's TestClient. 
# Cover: successful creation, listing, fetching by ID, updating, deleting, 404 for missing task,
# and validation error for bad payload. 

# Input: 

# # Test functions: 

# test_health_check() 

# test_create_task() 

# test_create_task_invalid_status() 

# test_get_tasks() 

# test_get_task_not_found() 

# test_update_task() 

# test_delete_task() 

# Output: 

# # Terminal output: 

# 7 passed in 0.45s 

# Constraints: 

# Use from fastapi.testclient import TestClient 

# Test both success (2xx) and failure (4xx) cases 

# Assert response status codes AND response body content 

# Minimum 7 test cases 
import pytest
from fastapi.testclient import TestClient
from main import app  

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_task():
    payload = {
        "title": "Write tests",
        "description": "Add pytest coverage",
        "status": "pending"
    }

    response = client.post("/tasks", json=payload)
    assert response.status_code == 201

    data = response.json()
    assert data["title"] == payload["title"]
    assert data["status"] == "pending"
    assert "id" in data


def test_create_task_invalid_status():
    payload = {
        "title": "Invalid task",
        "status": "in-progress"  
    }

    response = client.post("/tasks", json=payload)
    assert response.status_code == 422
    assert "detail" in response.json()


def test_get_tasks():
    response = client.get("/tasks")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)


def test_get_task_not_found():
    response = client.get("/tasks/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_update_task():
    # Create a task first
    create_response = client.post(
        "/tasks",
        json={"title": "Old title", "status": "pending"}
    )
    task_id = create_response.json()["id"]

    # Update the task
    update_payload = {
        "title": "Updated title",
        "status": "completed"
    }

    response = client.put(f"/tasks/{task_id}", json=update_payload)
    assert response.status_code == 200

    data = response.json()
    assert data["title"] == "Updated title"
    assert data["status"] == "completed"


def test_delete_task():
    # Create a task first
    create_response = client.post(
        "/tasks",
        json={"title": "Task to delete", "status": "pending"}
    )
    task_id = create_response.json()["id"]

    # Delete the task
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204

    # Verify deletion
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404
    

test_health_check() 

test_create_task() 

test_create_task_invalid_status() 

test_get_tasks() 

test_get_task_not_found() 

test_update_task() 

test_delete_task() 