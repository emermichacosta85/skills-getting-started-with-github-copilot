from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def reset_activities():
    activities.clear()
    activities.update(
        {
            "Chess Club": {
                "description": "Learn strategies and compete in chess tournaments",
                "schedule": "Fridays, 3:30 PM - 5:00 PM",
                "max_participants": 12,
                "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
            }
        }
    )


def test_signup_prevents_duplicates():
    reset_activities()

    response = client.post("/activities/Chess Club/signup?email=michael@mergington.edu")

    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()


def test_unregister_participant():
    reset_activities()
    email = "student@mergington.edu"
    activities["Chess Club"]["participants"].append(email)

    response = client.delete(f"/activities/Chess Club/signup?email={email}")

    assert response.status_code == 200
    assert email not in activities["Chess Club"]["participants"]
