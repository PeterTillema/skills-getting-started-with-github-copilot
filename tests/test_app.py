from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_duplicate_signup_is_rejected():
    activity_name = "Chess Club"
    email = "duplicate-test@mergington.edu"

    # Ensure clean state for this email
    client.delete(f"/activities/{activity_name}/participants?email={email}")

    first = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert first.status_code == 200

    second = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert second.status_code == 400
    assert "already signed up" in second.json()["detail"].lower()


def test_participant_can_be_removed():
    activity_name = "Chess Club"
    email = "remove-test@mergington.edu"

    client.delete(f"/activities/{activity_name}/participants?email={email}")

    signup = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup.status_code == 200

    delete_response = client.delete(f"/activities/{activity_name}/participants?email={email}")
    assert delete_response.status_code == 200
    assert email not in client.get("/activities").json()[activity_name]["participants"]
