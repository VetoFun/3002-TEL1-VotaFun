import json


def test_create_room_route(test_client):
    # Define the data to be sent in the POST request
    data = {"room_id": "test_room"}

    # Send a POST request to the create_room_route endpoint
    response = test_client.post("/createroom", json=data)

    # Check the response status code
    assert response.status_code == 200

    # Parse the JSON response
    result = json.loads(response.data.decode("utf-8"))

    # Check the result for success
    assert result["success"] is True
    assert "message" in result
    assert test_client.database.query_room_data(room_id="test_room")


def test_delete_room_route(test_client):
    # Send a DELETE request to the delete_room_route endpoint
    room_id = "test_room"  # Replace with a valid room ID
    response = test_client.delete(f"/closeroom/{room_id}")

    # Check the response status code
    assert response.status_code == 200

    # Parse the JSON response
    result = json.loads(response.data.decode("utf-8"))

    # Check the result for success
    assert result["success"] is True
    assert "num_deleted" in result


def test_join_room_route(test_client):
    create_room_data = {"room_id": "test_room"}

    # Send a POST request to the create_room_route endpoint to create a room
    create_room_response = test_client.post("/createroom", json=create_room_data)

    # Check the response status code for room creation
    assert create_room_response.status_code == 200

    # Define the data to be sent in the POST request
    data = {"user_id": "user123", "username": "test_user"}

    # Send a POST request to the join_room_route endpoint
    room_id = "test_room"  # Replace with a valid room ID
    response = test_client.post(f"/joinroom/{room_id}/users", json=data)

    # Check the response status code
    assert response.status_code == 200

    # Parse the JSON response
    result = json.loads(response.data.decode("utf-8"))

    # Check the result for success
    assert result["success"] is True
    assert "num_users" in result


def test_leave_room_route(test_client):
    create_room_data = {"room_id": "test_room"}

    # Send a POST request to the create_room_route endpoint to create a room
    create_room_response = test_client.post("/createroom", json=create_room_data)

    # Check the response status code for room creation
    assert create_room_response.status_code == 200

    add_user_data = {"user_id": "user123", "username": "test_user"}

    response = test_client.post("/joinroom/test_room/users", json=add_user_data)

    # Check the response status code for room creation
    assert response.status_code == 200

    # Send a DELETE request to the leave_room_route endpoint
    room_id = "test_room"  # Replace with a valid room ID
    user_id = "user123"  # Replace with a valid user ID
    response = test_client.delete(f"/leaveroom/{room_id}/users/{user_id}")

    # Check the response status code
    assert response.status_code == 200

    # Parse the JSON response
    result = json.loads(response.data.decode("utf-8"))

    # Check the result for success
    assert result["success"] is True
    assert "num_users" in result
    assert "is_host" in result


def test_get_all_users_route(test_client):
    create_room_data = {"room_id": "test_room"}

    # Send a POST request to the create_room_route endpoint to create a room
    create_room_response = test_client.post("/createroom", json=create_room_data)

    # Check the response status code for room creation
    assert create_room_response.status_code == 200
    # Send a GET request to the get_all_users_route endpoint
    room_id = "test_room"  # Replace with a valid room ID
    response = test_client.get(f"/rooms/{room_id}/getusers")

    # Check the response status code
    assert response.status_code == 200

    # Parse the JSON response
    result = json.loads(response.data.decode("utf-8"))

    # Check the result for success
    assert result["success"] is True
    assert "users" in result


def test_change_host_route(test_client):
    create_room_data = {"room_id": "test_room"}

    # Send a POST request to the create_room_route endpoint to create a room
    create_room_response = test_client.post("/createroom", json=create_room_data)

    # Check the response status code for room creation
    assert create_room_response.status_code == 200
    # Define the data to be sent in the PUT request
    data = {"new_hostid": "new_host123"}

    # Send a PUT request to the change_host_route endpoint
    room_id = "test_room"  # Replace with a valid room ID
    response = test_client.put(f"/rooms/{room_id}/changehost", json=data)

    # Check the response status code
    assert response.status_code == 200

    # Parse the JSON response
    result = json.loads(response.data.decode("utf-8"))

    # Check the result for success
    assert result["success"] is True
