from flask import request, copy_current_request_context
from flask_socketio import (
    Namespace,
    send,
    join_room,
    leave_room,
    close_room,
    disconnect,
    emit,
)
from flask import current_app as app
from time import sleep
from datetime import datetime
import threading

from src.logger import logger
from ..config import Config


class RoomManagement(Namespace):
    def on_connect(self):
        logger.info(f"Socket connected: {request.sid}")
        send("Socket connected successfully")

    def on_disconnect(self):
        logger.info(f"Socket disconnected: {request.sid}")

        try:
            # room before disconnect
            room_id = app.database.query_room_id_from_user_id(user_id=request.sid)
            room_users, is_host = app.database.remove_user(
                room_id=room_id, user_id=request.sid
            )
            # if the person that disconnect is a host, and there are more people in the room
            if is_host and len(room_users) > 0:
                new_host = room_users[0]
                app.database.change_host(
                    room_id=room_id, new_host_id=new_host["user_id"]
                )
                send(
                    f"Host changed to {new_host['username']}",
                    to=room_id,
                    namespace="/room-management",
                )
            elif len(room_users) == 0:
                app.database.remove_room_data(room_id=room_id)
                send(f"Room {room_id} has been closed", broadcast=True)
        except KeyError as e:
            logger.info(e)

        send("Socket disconnected successfully")

    def on_join_room(self, data):
        room_id = data["room_id"]
        user_name = data["user_name"]
        try:
            join_room(room_id)

            # Add user to database
            app.database.add_user(
                room_id=room_id, user_id=request.sid, username=user_name
            )
            # Send message to all users in room
            send(f"{user_name} has joined the room {room_id}", to=room_id)
        except Exception as e:
            # User fails to join room, either room has started or room is at max capacity.
            logger.info(e)
            send(f"{user_name} failed to join room {room_id} due to {e}", to=room_id)

    def on_leave_room(self, data):
        room_id = data["room_id"]
        user_name = data["user_name"]
        leave_room(room_id)

        try:
            # Remove user from database
            room_users, is_host = app.database.remove_user(
                room_id=room_id, user_id=request.sid
            )

            # room_data = app.database.query_room_data(room_id=room_id)
            if len(room_users) == 0:
                # Remove room from database
                self.on_close_room(data)

            # Send message to all users in room
            send(f"{user_name} has left the room {room_id}", to=room_id)
        except Exception as e:
            logger.info(e)

    def on_close_room(self, data):
        room_id = data["room_id"]
        close_room(room_id)

        # Remove room from database
        app.database.remove_room_data(room_id=room_id)

        # Send message to all users in room
        send(f"Room {room_id} has been closed", broadcast=True)

    def on_start_room(self, data):
        room_id = data["room_id"]
        try:
            app.database.start_room(room_id=room_id)
            # Send message to all users in room
            send(f"Room {room_id} has started", broadcast=True)
        except Exception as e:
            logger.info(e)

    def on_kick_user(self, data):
        room_id = data["room_id"]
        # user to kick
        kick_user_id = data["kick_user_id"]
        kick_user_name = data["kick_user_name"]
        try:
            app.database.kick_user(
                room_id=room_id, request_user_id=request.sid, kick_user_id=kick_user_id
            )
            # remove the user
            disconnect(sid=kick_user_id)
            # Send message to all users in room
            send(f"{kick_user_name} has been kicked by the host", to=room_id)
        except Exception as e:
            logger.info(e)

    def on_vote_option(self, data):
        room_id = data["room_id"]
        question_id = data["question_id"]
        option_id = data["option_id"]
        user_name = data["user_name"]

        try:
            app.database.increment_vote(
                room_id=room_id, question_id=question_id, option_id=option_id
            )

            send(
                f"{user_name} has voted {option_id} for {question_id}",
                to=room_id,
            )
        except Exception as e:
            logger.info(e)

    def on_start_round(self, data):
        # todo: add logic for getting questions and emit to the frontend
        # pesudocode
        # reply = llm.get_reply()
        # emit the reply to the frontend
        # emit("question", reply, namespace=Namespace)
        # get_reply() will handle storing questions and options into the database, as well as updating the time.
        # maybe an if statment to check if questions or activities are returned.
        # if questions start the countdown thread
        # reply will be a json in the form of
        # reply = {
        #     "question": "Question text",
        #     "question_id": "Question id",
        #     "options": {
        #         "1": "option 1" # etc
        #     },
        #     "num_of_options": 1
        # }
        # reply = {
        #     "activities": {
        #         "1": "activity 1" # etc
        #     },
        #     "num_of_activity": 1
        # }
        # start the countdown
        room_id = data["room_id"]

        @copy_current_request_context
        def countdown_round():
            sleep(Config.TIMER)
            with app.app_context():
                emit(
                    "end_round",
                    {"event": f"Round ended for {room_id}"},
                    namespace="/room-management",
                )

        countdown_thread = threading.Thread(target=countdown_round)
        countdown_thread.start()
        try:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            app.database.update_room_activity_time(
                room_id=room_id, activity_time=current_time
            )
        except Exception as e:
            logger.info(e)

    def on_set_room_properties(self, data):
        room_activity = data["room_activity"]
        room_location = data["room_location"]
        room_id = data["room_id"]

        try:
            app.database.set_room_properties(
                room_id=room_id,
                room_location=room_location,
                room_activity=room_activity,
                requesting_user_id=request.sid,
            )
            send(
                f"Room {room_id} has set the activity to {room_activity} and location to {room_location}",
                to=room_id,
            )
        except Exception as e:
            logger.info(e)
