from flask import request
from flask_socketio import Namespace, send, join_room, leave_room, close_room
from flask import current_app as app

from src.logger import logger


class RoomManagement(Namespace):
    def on_connect(self):
        logger.info(f"Socket connected: {request.sid}")
        send("Socket connected successfully")

    def on_disconnect(self):
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
                    send(
                        f"Host changed to {new_host_name}",
                        to=room_id,
                        namespace="/room-management",
                    )
                    # Remove user
                    app.database.remove_user(room_id=room_id, user_id=request.sid)
                else:
                    app.database.remove_room_data(room_id=room_id)
                    send(f"Room {room_id} has been closed", broadcast=True)
        except KeyError:
            pass

        send("Socket disconnected successfully")

    def on_join_room(self, data):
        room_id = data["room_id"]
        user_name = data["user_name"]

        room_data = app.database.query_room_data(room_id=room_id)
        if room_data is None:
            send(f"Room {room_id} does not exist")
            return

        if room_data.number_of_user == room_data.max_capacity:
            send(f"Room {room_id} is full")
            return

        join_room(room_id)

        # Add user to database
        app.database.add_user(room_id=room_id, user_id=request.sid, username=user_name)

        # Send message to all users in room
        send(f"{user_name} has joined the room {room_id}", to=room_id)

    def on_leave_room(self, data):
        room_id = data["room_id"]
        user_name = data["user_name"]
        leave_room(room_id)

        # Remove user from database
        app.database.remove_user(room_id=room_id, user_id=request.sid)

        room_data = app.database.query_room_data(room_id=room_id)
        if len(room_data.users) == 0:
            # Remove room from database
            self.on_close_room(data)

        # Send message to all users in room
        send(f"{user_name} has left the room {room_id}", to=room_id)

    def on_close_room(self, data):
        room_id = data["room_id"]
        close_room(room_id)

        # Remove room from database
        app.database.remove_room_data(room_id=room_id)

        # Send message to all users in room
        send(f"Room {room_id} has been closed", broadcast=True)