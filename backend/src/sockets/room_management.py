from flask import jsonify, request
from flask_socketio import Namespace, emit, send, join_room, leave_room, close_room, rooms
from flask import current_app as app

from src.logger import logger
from src.utils.Room import create_room_func


def list_users(room_id):
    """
    List all users in a room.
    :param room_id: room id
    :return: list of users in the room
    """
    room_data = app.database.query_room_data(room_id=room_id)
    return [
        {
            "user_id": user.user_id,
            "user_name": user.user_name,
            "is_host": room_data.host_id == user.user_id
        } for user in room_data.users]


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

    def on_create_room(self, data):
        """
        Route to handle post request to "/createroom".
        :return: response code 200 if the operation succeed, otherwise response code 500 is returned.
        """
        database = app.database
        try:
            result = create_room_func(data, database)
            emit('create_room', result)
        except Exception:
            return {"success": False, "error": "Internal Server Error"}, 500

    def on_join_room(self, data):
        print(data)
        room_id = data["room_id"]
        user_name = data["user_name"]

        room_data = app.database.query_room_data(room_id=room_id)
        if room_data is None:
            send(f"Room {room_id} does not exist")
            return

        if room_data.number_of_user == room_data.max_capacity:
            send(f"Room {room_id} is full")
            return

        join_room(room_id, request.sid)
        print(rooms())

        # Add user to database
        app.database.add_user(room_id=room_id, user_id=request.sid, username=user_name)
        room_data = app.database.query_room_data(room_id=room_id)

        if room_data.number_of_user == 1:
            # Set host
            room_data.host_id = request.sid
            app.database.store_room_data(room_id=room_id, room_data=room_data)

        # Send message to all users in room
        emit('join_room', {
            "success": True,
            "room_id": room_id,
            "user_id": request.sid,
            "user_name": user_name,
            "is_host": room_data.host_id == request.sid
        }, to=room_id)
        emit('update_room', list_users(room_id), to=room_id)

    def on_leave_room(self, data):
        room_id = data["room_id"]
        user_name = data["user_name"]
        leave_room(room_id, request.sid)

        # Remove user from database
        app.database.remove_user(room_id=room_id, user_id=request.sid)

        room_data = app.database.query_room_data(room_id=room_id)
        if len(room_data.users) == 0:
            # Remove room from database
            self.on_close_room(data)

        # Send message to all users in room
        print(f"{user_name} has left the room {room_id}")
        send(f"{user_name} has left the room {room_id}", to=room_id)

    def on_close_room(self, data):
        room_id = data["room_id"]
        close_room(room_id)

        # Remove room from database
        app.database.remove_room_data(room_id=room_id)

        # Send message to all users in room
        send(f"Room {room_id} has been closed", broadcast=True)
