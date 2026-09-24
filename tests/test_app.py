from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_signup_adds_participant_successfully():
    # Arrange
    from src import app as app_module

    activity_name = "Science Club"
    email = "newstudent@mergington.edu"
    app_module.activities[activity_name]["participants"] = []

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert email in app_module.activities[activity_name]["participants"]
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"


def test_signup_rejects_duplicate_email():
    # Arrange
    from src import app as app_module

    activity_name = "Science Club"
    email = "student1@mergington.edu"
    app_module.activities[activity_name]["participants"] = [email]

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()


def test_signup_returns_404_for_unknown_activity():
    # Arrange
    activity_name = "Nonexistent Club"
    email = "student1@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_participant_removes_email():
    # Arrange
    from src import app as app_module

    activity_name = "Basketball Club"
    removed_email = "student1@mergington.edu"
    remaining_email = "student2@mergington.edu"
    app_module.activities[activity_name]["participants"] = [removed_email, remaining_email]

    # Act
    response = client.delete(f"/activities/{activity_name}/participants?email={removed_email}")

    # Assert
    assert response.status_code == 200
    assert removed_email not in app_module.activities[activity_name]["participants"]
    assert remaining_email in app_module.activities[activity_name]["participants"]
