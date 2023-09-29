import pytest
from flask_socketio import SocketIOTestClient

from src.app import create_app, socketio
from src.database.Database import Database
from src.database.User import User  # noqa


@pytest.fixture
def charles_data():
    return {"room_id": "12345", "user_id": "1", "user_name": "Charles"}


@pytest.fixture
def roy_data():
    return {"room_id": "12345", "user_id": "2", "user_name": "Roy"}


@pytest.fixture
def kick_user_data():
    return {"room_id": "12345", "kick_user_id": "2", "kick_user_name": "Roy"}


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
    socketio.init_app(app)
    app.testing = True
    client1 = SocketIOTestClient(app, socketio)
    client2 = SocketIOTestClient(app, socketio)

    # Create a room with the two clients
    _create_room_with_2_people(
        client1, client2, server_namespace, charles_data, roy_data
    )

    yield client1, client2, app.database
    if client1.is_connected():
        client1.disconnect()
    if client2.is_connected():
        client2.disconnect()


def test_connect(clients):
    client1, client2, mock_database = clients
    assert client1.is_connected() is True
    assert client2.is_connected() is True


def test_join_room(clients, server_namespace):
    client1, client2, mock_database = clients

    # Assert correct response is sent to both clients
    response1 = client1.get_received(namespace=server_namespace)
    assert response1[1]["args"] == "Charles has joined the room 12345"
    response2 = client2.get_received(namespace=server_namespace)
    assert (
        response1[2]["args"] == response2[1]["args"] == "Roy has joined the room 12345"
    )


# def test_leave_room(clients, server_namespace, charles_data):
#     # Todo: fix test case
#     client1, client2, mock_database = clients
#
#     mocker_users = [User("1", "Charles"), User("2", "Roy")]
#     mock_database.query_room_data.return_value.users = mocker_users
#
#     # First client leaves room
#     client1.emit(
#         "leave_room",
#         charles_data,
#         namespace=server_namespace,
#     )
#
#     # Assert correct response is sent to client2 (still in the room)
#     response2 = client2.get_received(namespace=server_namespace)
#     mocker_users = [User("2", "Roy")]
#     print(mock_database.query_room_data.return_value.users) #= mocker_users
#
#     assert response2[2]["args"] == "Charles has left the room 12345"


def test_close_room(clients, server_namespace):
    client1, client2, mock_database = clients

    client1.emit(
        "close_room",
        {"room_id": "12345"},
        namespace=server_namespace,
    )

    # Assert correct response is sent to both clients
    response1 = client1.get_received(namespace=server_namespace)
    response2 = client2.get_received(namespace=server_namespace)
    assert response1[3]["args"] == response2[2]["args"] == "Room 12345 has been closed"


# def test_change_host(clients, server_namespace, mocker):
#     # Todo: fix test case
#     client1, client2, mock_database = clients
#
#     # Mock host_id is the same as request.sid
#     mock_database.query_room_id_from_user_id.return_value = "12345"
#     mock_database.query_room_data.return_value.users = [
#         User("1", "Charles"),
#         User("2", "Roy"),
#     ]
#     mock_database.query_room_data.return_value.host_id.__eq__.return_value = True
#
#     client1.disconnect(namespace=server_namespace)
#     response2 = client2.get_received(namespace=server_namespace)
#     assert response2[2]["args"] == "Host changed to Roy"


def test_vote_option(clients, server_namespace, charles_voting_data, roy_voting_data):
    client1, client2, mock_database = clients

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
    assert response2[2]["args"] == (
        f"{roy_voting_data['user_name']} "
        f"has voted {roy_voting_data['option_id']} for {roy_voting_data['question_id']}"
    )
    assert response1[3]["args"] == (
        f"{charles_voting_data['user_name']} has voted "
        f"{charles_voting_data['option_id']} for {charles_voting_data['question_id']}"
    )
