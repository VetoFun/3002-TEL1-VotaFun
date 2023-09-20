# from flask import request
from flask_socketio import Namespace
from .. import socketio


class RoomManagement(Namespace):
    def on_connect(self):
        print('Client connected to my namespace')

    def on_disconnect(self):
        print('Client disconnected from my namespace')

    def on_join_room(self, data):
        # TODO: add user to database
        print(data)
        room_id = data["RoomID"]
        user_name = data["UserName"]
        print(f"{user_name} has joined the room {room_id}")
        # socketio.join_room(room_id)
        socketio.send(f"{user_name} has joined the room {room_id}", to=room_id)

    def on_leave_room(self, data):
        # TODO: remove user from database
        room_id = data["RoomID"]
        user_name = data["UserName"]
        socketio.leave_room(room_id)
        socketio.send(f"{user_name} has left the room {room_id}", to=room_id)

    def on_close_room(self, data):
        # TODO: remove room and all users from database
        room_id = data["RoomID"]
        socketio.close_room(room_id)
        socketio.send(f"Room {room_id} has been closed", broadcast=True)

    def on_change_host(self, data):
        # TODO: verify the client socket is autherized to change host
        room_id = data["RoomID"]
        host_name = data["HostName"]
        socketio.send(
            f"{host_name} has become the new host of room {room_id}", to=room_id
        )

# @socketio.on("connect", namespace="/server/room-management")
# def handle_connect():
#     print(f"Socket connected: {request.sid}")
#     socketio.send("Socket connected successfully")


# @socketio.on("disconnect", namespace="/server/room-management")
# def handle_disconnect():
#     print(f"Socket disconnected: {request.sid}")
#     socketio.send("Socket disconnected successfully")


# @socketio.on("join_room", namespace="/server/room-management")
# def handle_join_room(data):
#     # TODO: add user to database
#     room_id = data["RoomID"]
#     user_name = data["UserName"]
#     socketio.join_room(room_id)
#     socketio.send(f"{user_name} has joined the room {room_id}", to=room_id)


# @socketio.on("leave_room", namespace="/server/room-management")
# def handle_leave_room(data):
#     # TODO: remove user from database
#     room_id = data["RoomID"]
#     user_name = data["UserName"]
#     socketio.leave_room(room_id)
#     socketio.send(f"{user_name} has left the room {room_id}", to=room_id)


# @socketio.on("close_room", namespace="/server/room-management")
# def handle_close_room(data):
#     # TODO: remove room and all users from database
#     room_id = data["RoomID"]
#     socketio.close_room(room_id)
#     socketio.send(f"Room {room_id} has been closed", broadcast=True)


# @socketio.on("change_host", namespace="/server/room-management")
# def handle_change_host(data):
#     # TODO: verify the client socket is autherized to change host
#     room_id = data["RoomID"]
#     host_name = data["HostName"]
#     socketio.send(
#         f"{host_name} has become the new host of room {room_id}", to=room_id
#     )
