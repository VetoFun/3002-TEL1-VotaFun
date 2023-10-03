from flask import request, copy_current_request_context
from flask_socketio import (
    Namespace,
    join_room,
    leave_room,
    close_room,
    disconnect,
    emit,
)
from flask import current_app as app
from time import sleep
import threading
import traceback

from src.logger import logger
from ..config import Config
from dataclasses import dataclass, asdict


@dataclass
class Message:
    success: bool = None
    message: str = None
    data: dict = None


class RoomManagement(Namespace):
    def on_connect(self):
        logger.info(f"Socket connected: {request.sid}")
        message = Message(success=True, message=f"${request.sid} connected successfully.")
        emit(
            "client_connection_event",
            asdict(message),
            to=request.sid,
        )

    def on_disconnect(self):
        logger.info(f"Socket disconnected: {request.sid}")
        message = Message()
        event_name = "disconnect_event"

        try:
            # room before disconnect
            room_id = app.database.query_room_id_from_user_id(user_id=request.sid)

            # remove user from database
            room_users, is_host = app.database.remove_user(
                room_id=room_id, user_id=request.sid
            )
            message.success = True

            if not is_host:
                message.message = f"{request.sid} has disconnected."
            elif is_host and len(room_users) > 0:
                new_host = app.database.query_room_data(room_id=room_id).host_name
                message.message = (
                    f"Host {request.sid} has disconnected. Host changed to {new_host}."
                )
                message.data = {"new_host": new_host}
            elif len(room_users) == 0:
                self.on_close_room(data={"room_id": room_id})

            emit(
                event_name,
                asdict(message),
                to=room_id,
            )
            room = app.database.query_room_data(room_id=room_id)
            self.broadcast_room_user_change("leave_room_event", room)

        except Exception as e:
            logger.info(e)
            message.success = False
            message.message = (
                f"Something went wrong, unable to remove user from database due to {e}"
            )
            emit(
                event_name,
                asdict(message),
                broadcast=True,
            )

    def on_create_room(self, data):
        event_name = "client_create_room_event"
        message = Message()

        try:
            # Add room to database
            room = app.database.create_room()
            logger.info(room)

            # Send message to all users in room
            message.success = True
            message.message = f"room {room.room_id} has been created."
            message.data = {"room": room.to_dict()}
            emit(
                event_name,
                asdict(message),
                to=request.sid,
            )

        except Exception as e:
            logger.error(f'create_room: ${print(traceback.format_exc()) }${e}')
            message.success = False
            message.message = f"failed to create room due to {e}."
            emit(
                event_name,
                asdict(message),
                to=request.sid,
            )

    def on_join_room(self, data):
        room_id = data["room_id"]
        user_name = data["user_name"]
        user_id = request.sid

        message = Message()
        event_name = "join_room_event"

        try:
            # Add user to database
            app.database.add_user(room_id=room_id, user_id=user_id, username=user_name)

            join_room(room_id)
            room = app.database.query_room_data(room_id=room_id)

            message.success = True
            message.message = f"{user_name} has joined room {room_id}."
            message.data = {"room": room.to_dict()}
            emit(
                "client_join_room_event",
                asdict(message),
                to=request.sid,
            )
            self.broadcast_room_user_change("join_room_event", room)

        except Exception as e:
            # User fails to join room, either room has started or room is at max capacity.
            logger.error(f'join_room: ${e}')
            message.success = False
            message.message = f"{user_name} failed to join room {room_id} due to {e}."

            emit(
                'client_join_room_event',
                asdict(message),
                to=request.sid,
            )

    def on_leave_room(self, data):
        room_id = data["room_id"]
        user_name = data["user_name"]
        leave_room(room_id)

        message = Message()
        event_name = "leave_room_event"

        try:
            # Remove user from database
            room_users, is_host = app.database.remove_user(
                room_id=room_id, user_id=request.sid
            )
            message.success = True

            if not is_host:
                message.message = f"{user_name} has left room {room_id}."
            elif is_host and len(room_users) > 0:
                new_host = app.database.query_room_data(room_id=room_id).host_name
                message.message = (
                    f"Host {user_name} has left. Host changed to {new_host}."
                )
                message.data = {"new_host": new_host}
            elif len(room_users) == 0:
                self.on_close_room(data={"room_id": room_id})

            room = app.database.query_room_data(room_id=room_id)
            self.broadcast_room_user_change("leave_room_event", room)

        except Exception as e:
            logger.info(e)
            message.success = False
            message.message = f"Something went wrong, unable to leave room due to {e}."

    def on_close_room(self, data):
        room_id = data["room_id"]
        requesting_user_id = request.sid

        message = Message()
        event_name = "close_room_event"

        # Check if room is empty or if user is host
        room_data = app.database.query_room_data(room_id=room_id)
        if len(room_data.users) > 0 and not app.database.is_host(
            room_id=room_id, user_id=requesting_user_id
        ):
            message.success = False
            message.message = "Only the host can close the room."
            emit(
                event_name,
                asdict(message),
                to=request.sid,
            )
            return

        try:
            # Remove room from database
            app.database.remove_room_data(room_id=room_id)

            close_room(room_id)

            message.success = True
            message.message = f"Room {room_id} has been closed."

        except Exception as e:
            logger.info(e)
            message.success = False
            message.message = f"Something went wrong, unable to close room due to {e}."

        # Send message to all users in room
        emit(
            event_name,
            asdict(message),
            to=room_id,
        )

    def on_start_room(self, data):
        room_activity = data["room_activity"]
        room_location = data["room_location"]
        room_id = data["room_id"]

        message = Message()
        event_name = "start_room_event"

        try:
            app.database.start_room(
                room_id=room_id,
                room_location=room_location,
                room_activity=room_activity,
                requesting_user_id=request.sid,
            )

            message.success = True
            message.message = f"Room {room_id} has started."

        except Exception as e:
            logger.info(e)
            message.success = False
            message.message = f"Something went wrong, unable to start room due to {e}."

        # Send message to all users in room
        emit(
            event_name,
            asdict(message),
            to=room_id,
        )

    def on_kick_user(self, data):
        room_id = data["room_id"]
        user_id = data["user_id"]
        user_name = data["user_name"]
        request_user_id = request.sid

        message = Message()
        event_name = "kick_user_event"

        try:
            app.database.kick_user(
                room_id=room_id,
                request_user_id=request_user_id,
                kick_user_id=user_id,
            )
            disconnect(sid=user_id)
            message.success = True
            message.message = f"{user_name} has been kicked from room {room_id}."

        except Exception as e:
            logger.info(e)
            message.success = False
            message.message = (
                f"Something went wrong, unable to kick {user_name} due to {e}."
            )

        # Send message to all users in room
        emit(
            event_name,
            asdict(message),
            to=room_id,
        )

    def on_vote_option(self, data):
        room_id = data["room_id"]
        question_id = data["question_id"]
        option_id = data["option_id"]
        user_name = data["user_name"]

        message = Message()
        event_name = "vote_option_event"

        try:
            app.database.increment_vote(
                room_id=room_id, question_id=question_id, option_id=option_id
            )
            message.success = True
            message.message = f"{user_name} has voted {option_id} for {question_id}."

        except Exception as e:
            logger.info(e)
            message.success = False
            message.message = f"Something went wrong, unable to vote {option_id} for {question_id} due to {e}."

        # Send message to only the user who voted
        emit(
            event_name,
            asdict(message),
            to=request.sid,
        )

    def on_start_round(self, data):
        room_id = data["room_id"]

        message = Message()
        event_name = "start_round_event"

        try:
            # get_reply() will handle storing questions and options into the database, as well as updating the time.
            reply, type_of_reply = app.llm.get_reply(
                room_id=room_id, database=app.database
            )

            message.success = True
            message.message = f"Round started successfully for {room_id}."
            message.data = reply

            # Send message to all users in room
            emit(
                event_name,
                asdict(message),
                to=room_id,
            )

            # if reply is a question, start the countdown
            if type_of_reply == "question":

                @copy_current_request_context
                def countdown_round():
                    sleep(
                        Config.TIMER + 2
                    )  # add a buffer time of 2 seconds to ensure frontend timer are all up.
                    with app.app_context():
                        message = Message(
                            success=True, message=f"Round ended for {room_id}."
                        )
                        emit(
                            "end_round_event",
                            asdict(message),
                            to=room_id,
                        )

                countdown_thread = threading.Thread(target=countdown_round)
                countdown_thread.start()

        except Exception as e:
            logger.info(e)
            message.success = False
            message.message = f"Unable to start a round due to {e}."
            # Send message to all users in room
            emit(
                event_name,
                asdict(message),
                to=room_id,
            )

    def on_set_room_properties(self, data):
        room_activity = data["room_activity"]
        room_location = data["room_location"]
        room_id = data["room_id"]

        message = Message()
        event_name = "set_room_properties_event"

        try:
            room_data = app.database.query_room_data(room_id=room_id)
            room_data.room_activity = room_activity
            room_data.room_location = room_location
            app.database.store_room_data(room_id=room_id, room_data=room_data)

            message.success = True
            message.message = f"Room {room_id} has set the activity to {room_activity} and location to {room_location}."

        except Exception as e:
            logger.info(e)
            message.success = False
            message.message = f"Unable to set room properties due to {e}."

        # Send message to all users in room
        emit(
            event_name,
            asdict(message),
            to=room_id,
        )

    def broadcast_room_user_change(self, event_name, room):
        message = Message(
            success=True, message="Room state updated.", data={"room": room.to_dict()}
        )
        emit(event_name, asdict(message), to=room.room_id)
