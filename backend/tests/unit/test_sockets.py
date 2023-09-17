import pytest
from src.app import create_app, socketio
from flask_socketio import SocketIOTestClient


@pytest.fixture
def charles_data():
    return {"RoomID": "12345", "UserID": "1", "UserName": "Charles"}


@pytest.fixture
def roy_data():
    return {"RoomID": "12345", "UserID": "2", "UserName": "Roy"}


@pytest.fixture
def server_namespace():
    return "/server/room_management"


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
def clients(server_namespace, charles_data, roy_data):
    app = create_app()
    socketio.init_app(app)
    app.testing = True
    client1 = SocketIOTestClient(app, socketio)
    client2 = SocketIOTestClient(app, socketio)

    # Create a room with the two clients
    _create_room_with_2_people(
        client1, client2, server_namespace, charles_data, roy_data
    )

    yield client1, client2
    client1.disconnect()
    client2.disconnect()


def test_connect(clients):
    client1, client2 = clients
    assert client1.is_connected() is True
    assert client2.is_connected() is True


def test_join_room(clients, server_namespace):
    client1, client2 = clients

    # Assert correct response is sent to both clients
    response1 = client1.get_received(namespace=server_namespace)
    assert response1[0]["args"] == "Charles has joined the room 12345"
    response2 = client2.get_received(namespace=server_namespace)
    assert (
        response1[1]["args"] == response2[0]["args"] == "Roy has joined the room 12345"
    )


def test_leave_room(clients, server_namespace, charles_data):
    client1, client2 = clients

    # First client leaves room
    client1.emit(
        "leave_room",
        charles_data,
        namespace=server_namespace,
    )

    # Assert correct response is sent to client2 (still in the room)
    response2 = client2.get_received(namespace=server_namespace)
    assert response2[1]["args"] == "Charles has left the room 12345"


def test_close_room(clients, server_namespace):
    client1, client2 = clients

    client1.emit(
        "close_room",
        {"RoomID": "12345"},
        namespace=server_namespace,
    )

    # Assert correct response is sent to both clients
    response1 = client1.get_received(namespace=server_namespace)
    response2 = client2.get_received(namespace=server_namespace)
    assert response1[2]["args"] == response2[1]["args"] == "Room 12345 has been closed"


def test_change_host(clients, server_namespace):
    client1, client2 = clients

    client1.emit(
        "change_host",
        {"RoomID": "12345", "HostName": "Roy"},
        namespace=server_namespace,
    )

    # Assert correct response is sent to both clients
    response1 = client1.get_received(namespace=server_namespace)
    response2 = client2.get_received(namespace=server_namespace)
    assert (
        response1[2]["args"]
        == response2[1]["args"]
        == "Roy has become the new host of room 12345"
    )
