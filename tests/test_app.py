import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Basketball Team" in data

def test_signup_and_unregister():
    email = "testuser@mergington.edu"
    activity = "Basketball Team"
    # Ensure user is not already signed up
    client.post(f"/activities/{activity}/unregister", params={"email": email})
    # Sign up
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]
    # Try duplicate signup
    response_dup = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response_dup.status_code == 400
    # Unregister
    response_unreg = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert response_unreg.status_code == 200
    assert f"Removed {email}" in response_unreg.json()["message"]
    # Try duplicate unregister
    response_unreg2 = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert response_unreg2.status_code == 400

def test_signup_invalid_activity():
    response = client.post("/activities/Nonexistent/signup", params={"email": "foo@bar.com"})
    assert response.status_code == 404

def test_unregister_invalid_activity():
    response = client.post("/activities/Nonexistent/unregister", params={"email": "foo@bar.com"})
    assert response.status_code == 404
