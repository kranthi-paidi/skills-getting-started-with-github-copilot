import copy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture()
def client():
    original = copy.deepcopy(activities)
    try:
        yield TestClient(app)
    finally:
        activities.clear()
        activities.update(original)


def test_get_activities_returns_data(client):
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert "Soccer Team" in data
    assert "participants" in data["Soccer Team"]


def test_signup_adds_participant(client):
    activity_name = "Soccer Team"
    email = "newstudent@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    assert response.status_code == 200
    assert email in activities[activity_name]["participants"]


def test_unregister_removes_participant(client):
    activity_name = "Drama Club"
    email = "amelia@mergington.edu"

    assert email in activities[activity_name]["participants"]

    response = client.delete(
        f"/activities/{activity_name}/participants", params={"email": email}
    )

    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]
