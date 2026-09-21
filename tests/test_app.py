from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_duplicate_signup_is_rejected():
    # Arrange
    activity_name = "Chess Club"
    email = "duplicate-test@mergington.edu"
    client.delete(f"/activities/{activity_name}/participants?email={email}")

    # Act
    first_signup = client.post(f"/activities/{activity_name}/signup?email={email}")
    second_signup = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert first_signup.status_code == 200
    assert second_signup.status_code == 400
    assert "already signed up" in second_signup.json()["detail"].lower()


def test_participant_can_be_removed():
    # Arrange
    activity_name = "Chess Club"
    email = "remove-test@mergington.edu"
    client.delete(f"/activities/{activity_name}/participants?email={email}")

    # Act
    signup = client.post(f"/activities/{activity_name}/signup?email={email}")
    delete_response = client.delete(f"/activities/{activity_name}/participants?email={email}")
    activities_response = client.get("/activities")

    # Assert
    assert signup.status_code == 200
    assert delete_response.status_code == 200
    assert email not in activities_response.json()[activity_name]["participants"]
