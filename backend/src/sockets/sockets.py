from flask import request
from .. import socketio

@socketio.on("connect")
def handle_connect():
    print(f"Socket connected: {request.sid}")
    socketio.send("Socket connected successfully")


@socketio.on("disconnect")
def handle_disconnect():
    print(f"Socket disconnected: {request.sid}")
    socketio.send("Socket disconnected successfully")


@socketio.on("join_room", namespace="/server/room_management")
def handle_join_room(data):
    # TODO: add user to database
    room_id = data["RoomID"]
    user_name = data["UserName"]
    socketio.join_room(room_id)
    socketio.send(f"{user_name} has joined the room {room_id}", to=room_id)


@socketio.on("leave_room", namespace="/server/room_management")
def handle_leave_room(data):
    # TODO: remove user from database
    room_id = data["RoomID"]
    user_name = data["UserName"]
    socketio.leave_room(room_id)
    socketio.send(f"{user_name} has left the room {room_id}", to=room_id)


@socketio.on("close_room", namespace="/server/room_management")
def handle_close_room(data):
    # TODO: remove room and all users from database
    room_id = data["RoomID"]
    socketio.close_room(room_id)
    socketio.send(f"Room {room_id} has been closed", broadcast=True)


@socketio.on("change_host", namespace="/server/room_management")
def handle_change_host(data):
    # TODO: verify the client socket is autherized to change host
    room_id = data["RoomID"]
    host_name = data["HostName"]
    socketio.send(
        f"{host_name} has become the new host of room {room_id}", to=room_id
    )
