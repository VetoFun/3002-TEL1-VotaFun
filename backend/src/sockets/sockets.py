from flask import request
import flask_socketio
from flask import current_app as app
from src.logger import logger

socketio = flask_socketio.SocketIO(cors_allowed_origins="*")


@socketio.on("connect")
def handle_connect():
    logger.info(f"Socket connected: {request.sid}")
    flask_socketio.send("Socket connected successfully")


@socketio.on("disconnect")
def handle_disconnect():
    logger.info(f"Socket disconnected: {request.sid}")

    try:
        # room before disconnect
        room_id = app.database.query_room_id_from_user_id(user_id=request.sid)
        room_data = app.database.query_room_data(room_id=room_id)

        if room_data.host_id == request.sid:
            # Change host
            if len(room_data.users) > 1:
                room_data.host_id = room_data.users[1].user_id
                new_host_name = room_data.users[1].user_name
                app.database.store_room_data(room_id=room_id, room_data=room_data)
                flask_socketio.send(
                    f"Host changed to {new_host_name}",
                    to=room_id,
                    namespace="/server/room_management",
                )
                # Remove user
                app.database.remove_user(room_id=room_id, user_id=request.sid)
            else:
                app.database.remove_room_data(room_id=room_id)
                flask_socketio.send(f"Room {room_id} has been closed", broadcast=True)
    except KeyError:
        pass

    flask_socketio.send("Socket disconnected successfully")


@socketio.on("join_room", namespace="/server/room_management")
def handle_join_room(data):
    room_id = data["room_id"]
    user_name = data["user_name"]

    room_data = app.database.query_room_data(room_id=room_id)
    if room_data is None:
        flask_socketio.send(f"Room {room_id} does not exist")
        return

    if room_data.number_of_user == room_data.max_capacity:
        flask_socketio.send(f"Room {room_id} is full")
        return

    flask_socketio.join_room(room_id)

    # Add user to database
    app.database.add_user(room_id=room_id, user_id=request.sid, username=user_name)

    # Send message to all users in room
    flask_socketio.send(f"{user_name} has joined the room {room_id}", to=room_id)


@socketio.on("leave_room", namespace="/server/room_management")
def handle_leave_room(data):
    room_id = data["room_id"]
    user_name = data["user_name"]
    flask_socketio.leave_room(room_id)

    # Remove user from database
    app.database.remove_user(room_id=room_id, user_id=request.sid)

    room_data = app.database.query_room_data(room_id=room_id)
    if len(room_data.users) == 0:
        # Remove room from database
        handle_close_room(data)

    # Send message to all users in room
    flask_socketio.send(f"{user_name} has left the room {room_id}", to=room_id)


@socketio.on("close_room", namespace="/server/room_management")
def handle_close_room(data):
    room_id = data["room_id"]
    flask_socketio.close_room(room_id)

    # Remove room from database
    app.database.remove_room_data(room_id=room_id)

    # Send message to all users in room
    flask_socketio.send(f"Room {room_id} has been closed", broadcast=True)
