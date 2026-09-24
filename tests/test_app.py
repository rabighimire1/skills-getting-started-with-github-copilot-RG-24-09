from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_signup_rejects_duplicate_email():
    from src import app as app_module

    app_module.activities["Science Club"]["participants"] = ["student1@mergington.edu"]

    response = client.post("/activities/Science Club/signup?email=student1@mergington.edu")

    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()


def test_unregister_participant_removes_email():
    from src import app as app_module

    app_module.activities["Basketball Club"]["participants"] = [
        "student1@mergington.edu",
        "student2@mergington.edu",
    ]

    response = client.delete("/activities/Basketball Club/participants?email=student1@mergington.edu")

    assert response.status_code == 200
    assert "student1@mergington.edu" not in app_module.activities["Basketball Club"]["participants"]
    assert "student2@mergington.edu" in app_module.activities["Basketball Club"]["participants"]
