import pytest
from flask_socketio import SocketIOTestClient

from src.app import create_app, socketio
from src.database.Database import Database
from src.database.User import User  # noqa

from src.utils.LLM import LLM


@pytest.fixture
def charles_data():
    return {"room_id": "12345", "user_id": "1", "user_name": "Charles"}


@pytest.fixture
def roy_data():
    return {"room_id": "12345", "user_id": "2", "user_name": "Roy"}


@pytest.fixture
def kick_user_data():
    return {"room_id": "12345", "user_id": "2", "user_name": "Roy"}


@pytest.fixture
def charles_voting_data():
    return {
        "room_id": "12345",
        "question_id": "98765",
        "user_name": "Charles",
        "option_id": "1",
    }


@pytest.fixture
def roy_voting_data():
    return {
        "room_id": "12345",
        "question_id": "98765",
        "user_name": "Roy",
        "option_id": "2",
    }


@pytest.fixture
def room_properties():
    return {
        "room_activity": "food",
        "room_location": "center",
        "room_id": "12345",
    }


@pytest.fixture
def server_namespace():
    return "/room-management"


def _create_room_with_2_people(
    client1, client2, server_namespace, charles_data, roy_data
):
    client1.connect(namespace=server_namespace)
    client1.emit(
        "join_room",
        charles_data,
        namespace=server_namespace,
    )

    client2.connect(namespace=server_namespace)
    client2.emit(
        "join_room",
        roy_data,
        namespace=server_namespace,
    )


@pytest.fixture
def clients(server_namespace, charles_data, roy_data, mocker):
    app = create_app()
    app.database = mocker.MagicMock(spec=Database)
    app.database.query_room_id_from_user_id.return_value = None
    app.database.add_user.return_value.to_dict.return_value = "12345"
    app.llm = mocker.MagicMock(spec=LLM)
    socketio.init_app(app)
    app.testing = True
    client1 = SocketIOTestClient(app, socketio)
    client2 = SocketIOTestClient(app, socketio)

    # Create a room with the two clients
    _create_room_with_2_people(
        client1, client2, server_namespace, charles_data, roy_data
    )

    yield client1, client2, app.database, app.llm
    if client1.is_connected():
        client1.disconnect()
    if client2.is_connected():
        client2.disconnect()


def test_connect(clients):
    client1, client2, mock_database, mock_llm = clients
    assert client1.is_connected() is True
    assert client2.is_connected() is True


def test_join_room(clients, server_namespace):
    client1, client2, mock_database, mock_llm = clients

    # Assert correct response is sent to both clients
    response = client1.get_received(namespace=server_namespace)
    assert response[1]["args"][0]["message"] == "Charles has joined room 12345."


def test_leave_room(clients, server_namespace, charles_data, mocker):
    client1, client2, mock_database, mock_llm = clients
    mock_room = mocker.MagicMock()
    mock_database.remove_user.return_value = (mock_room, False, None)
    mock_room.number_of_users.return_value = 1

    # First client leaves room
    client1.emit(
        "leave_room",
        charles_data,
        namespace=server_namespace,
    )

    # Assert correct response is sent to client2 (still in the room)
    response2 = client2.get_received(namespace=server_namespace)
    assert response2[2]["name"] == "leave_room_event"


def test_close_room(clients, server_namespace):
    client1, client2, mock_database, mock_llm = clients
    mock_database.user_close_room.return_value = 1
    client1.emit(
        "close_room",
        {"room_id": "12345"},
        namespace=server_namespace,
    )

    # Assert correct response is sent to both clients
    response1 = client1.get_received(namespace=server_namespace)
    response2 = client2.get_received(namespace=server_namespace)
    assert response1[2]["name"] == response2[2]["name"] == "close_room_event"


def test_change_host(clients, server_namespace, charles_data, mocker):
    client1, client2, mock_database, mock_llm = clients

    mock_room = mocker.MagicMock()
    mock_database.remove_user.return_value = (mock_room, True, "new_host_id")
    mock_room.number_of_users.return_value = 1

    client1.emit(
        "leave_room",
        charles_data,
        namespace=server_namespace,
    )
    response2 = client2.get_received(namespace=server_namespace)
    print(response2)
    assert response2[2]["name"] == "leave_room_event"
    assert (
        response2[2]["args"][0]["message"]
        == "Host Charles has disconnected. Host changed to new_host_id."
    )


def test_kick_user(clients, server_namespace, kick_user_data, mocker):
    client1, client2, mock_database, mock_llm = clients
    mock_room = mocker.MagicMock()
    mock_database.kick_user.return_value = mock_room
    mock_room.to_dict.return_value = {}
    client1.emit(
        "kick_user",
        kick_user_data,
        namespace=server_namespace,
    )

    # Assert correct response is sent to client2 (still in the room)
    response2 = client2.get_received(namespace=server_namespace)
    assert response2[2]["args"][0]["message"] == "Roy has been kicked from room 12345."


def test_vote_option(clients, server_namespace, charles_voting_data, roy_voting_data):
    client1, client2, mock_database, mock_llm = clients

    client1.emit(
        "vote_option",
        charles_voting_data,
        namespace=server_namespace,
    )

    client2.emit(
        "vote_option",
        roy_voting_data,
        namespace=server_namespace,
    )

    # Assert correct response is sent to client1 and client2
    response1 = client1.get_received(namespace=server_namespace)
    response2 = client2.get_received(namespace=server_namespace)
    print(response1)
    print(response2)
    assert response2[2]["args"][0]["message"] == (
        f"{roy_voting_data['user_name']} "
        f"has voted {roy_voting_data['option_id']} for {roy_voting_data['question_id']}."
    )
    assert response1[2]["args"][0]["message"] == (
        f"{charles_voting_data['user_name']} has voted "
        f"{charles_voting_data['option_id']} for {charles_voting_data['question_id']}."
    )


def test_set_room_props(clients, server_namespace, room_properties, mocker):
    client1, client2, mock_database, mock_llm = clients
    mock_room = mocker.MagicMock()
    mock_database.set_room_properties.return_value = mock_room
    mock_room.to_dict.return_value = {}
    client1.emit(
        "set_room_properties",
        room_properties,
        namespace=server_namespace,
    )

    response1 = client1.get_received(namespace=server_namespace)
    expected_message = (
        f'Room 12345 has set the activity to {room_properties["room_activity"]}'
    )
    expected_message += f' and location to {room_properties["room_location"]}.'
    assert response1[2]["args"][0]["message"] == (
        f'Room 12345 has set the activity to {room_properties["room_activity"]}'
        f' and location to {room_properties["room_location"]}.'
    )


def test_start_room(clients, server_namespace, room_properties, mocker):
    client1, client2, mock_database, mock_llm = clients
    mock_room = mocker.MagicMock()
    mock_database.start_room.return_value = mock_room
    mock_room.to_dict.return_value = {}
    mock_result = mocker.MagicMock()
    mock_database.get_room_final_result.return_value = (True, mock_result)
    mock_result.to_dict.return_value = {}

    mock_llm.get_reply.return_value = ("", "activities")

    client1.emit(
        "start_room",
        room_properties,
        namespace=server_namespace,
    )

    response1 = client1.get_received(namespace=server_namespace)
    assert response1[2]["args"][0]["message"] == "Room 12345 has started."


def test_disconnect(clients, server_namespace, mocker):
    client1, client2, mock_database, mock_llm = clients
    mock_database.query_room_id_from_user_id.return_value = "12345"
    mock_room = mocker.MagicMock()
    mock_room.number_of_users.return_value = 1
    mock_room.to_dict.return_value = {}
    mock_room.room_id = "12345"
    mock_database.remove_user.return_value = (mock_room, False, None)

    client1.disconnect(namespace=server_namespace)

    response2 = client2.get_received(namespace=server_namespace)
    assert response2[2]["name"] == "disconnect_event"
    assert response2[2]["args"][0]["success"]


def test_create_room(clients, server_namespace, mocker):
    client1, client2, mock_database, mock_llm = clients
    mock_room = mocker.MagicMock()
    mock_room.to_dict.return_value = {}
    mock_room.room_id = "23456"
    mock_database.create_room.return_value = mock_room

    client1.emit(
        "create_room",
        {},
        namespace=server_namespace,
    )

    response1 = client1.get_received(namespace=server_namespace)
    assert response1[2]["args"][0]["message"] == "room 23456 has been created."


def test_check_room_exist(clients, server_namespace, mocker):
    client1, client2, mock_database, mock_llm = clients
    mock_database.is_room_exist.return_value = True

    client1.emit(
        "check_room_exist",
        {"room_id": "12345"},
        namespace=server_namespace,
    )

    response1 = client1.get_received(namespace=server_namespace)
    assert response1[2]["args"][0]["message"] == "Room 12345 exists."
