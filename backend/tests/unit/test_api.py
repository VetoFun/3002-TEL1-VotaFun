import json
import pytest
from src.app import create_app


@pytest.fixture(scope="module")
def test_client():
    flask_app = create_app()
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client


def test_create_room_success(test_client):
    data = {
        "username": "John",
        "host_id": "123456",
        "location": "west",
        "activity": "indoor",
    }
    response = test_client.post(
        "/createroom",
        data=json.dumps(data),
        headers={"Content-Type": "application/json"},
    )
    response_data = response.get_json()
    assert (
        response.status_code == 200
        and response_data["success"]
        and "room_id" in response_data
    )
    return response_data["room_id"]


def test_create_room_fail(test_client):
    data = {"username": "John", "host_id": "123456", "location": "west"}
    response = test_client.post(
        "/createroom",
        data=json.dumps(data),
        headers={"Content-Type": "application/json"},
    )
    response_data = response.get_json()
    assert response.status_code == 500 and not response_data["success"]


def test_join_room_success(test_client):
    room_id = test_create_room_success(test_client)
    data = {"username": "Eve", "user_id": "223456"}
    response = test_client.post(
        f"/joinroom/{room_id}/users",
        data=json.dumps(data),
        headers={"Content-Type": "application/json"},
    )
    response_data = response.get_json()
    assert response.status_code == 200 and response_data["success"]


def test_get_all_users_success(test_client):
    room_id = test_create_room_success(test_client)
    response = test_client.get(f"/rooms/{room_id}/getusers")
    response_data = response.get_json()
    assert response.status_code == 200 and len(response_data["users"]) == 1


def test_get_all_users_fail(test_client):
    response = test_client.get("/rooms/aucsdjhbd/getusers")
    response_data = response.get_json()
    assert response.status_code == 500 and "error" in response_data
