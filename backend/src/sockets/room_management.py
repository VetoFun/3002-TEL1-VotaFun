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

from src.logger import logger
from ..config import Config


class RoomManagement(Namespace):
    def on_connect(self):
        logger.info(f"Socket connected: {request.sid}")
        emit(
            "connection_event",
            {"success": True, "message": "Socket connected successfully."},
        )

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
                emit(
                    "disconnect_event",
                    {
                        "success": True,
                        "message": f"Someone disconnected. Host changed to {new_host['username']}.",
                        "users": room_users,
                        "new_host": new_host["username"],
                    },
                    to=room_id,
                )
            elif len(room_users) == 0:
                app.database.remove_room_data(room_id=room_id)
                emit(
                    "disconnect_event",
                    {
                        "success": True,
                        "message": f"Someone disconnected. No one left in the room. Room {room_id} has been closed.",
                        "users": room_users,
                        "new_host": "",
                    },
                    broadcast=True,
                )
        except KeyError as e:
            logger.info(e)
            emit(
                "disconnect_event",
                {
                    "success": False,
                    "message": f"Something went wrong, unable to disconnect due to {e}",
                },
                broadcast=True,
            )

    def on_join_room(self, data):
        room_id = data["room_id"]
        user_name = data["user_name"]
        try:
            join_room(room_id)

            # Add user to database
            room_users = app.database.add_user(
                room_id=room_id, user_id=request.sid, username=user_name
            )
            # Send message to all users in room
            emit(
                "join_room_event",
                {
                    "success": True,
                    "users": room_users,
                    "message": f"{user_name} has joined the room {room_id}.",
                },
                to=room_id,
            )
        except Exception as e:
            # User fails to join room, either room has started or room is at max capacity.
            logger.info(e)
            emit(
                "join_room_event",
                {
                    "success": False,
                    "message": f"{user_name} failed to join room {room_id} due to {e}.",
                },
                to=room_id,
            )

    def on_leave_room(self, data):
        room_id = data["room_id"]
        user_name = data["user_name"]
        leave_room(room_id)

        try:
            # Remove user from database
            room_users, is_host = app.database.remove_user(
                room_id=room_id, user_id=request.sid
            )
            # if a host leaves
            if is_host and len(room_users) > 0:
                new_host = room_users[0]
                app.database.change_host(
                    room_id=room_id, new_host_id=new_host["user_id"]
                )
                emit(
                    "leave_event",
                    {
                        "success": True,
                        "message": f"{user_name} has left the room {room_id}. Host changed to {new_host['username']}.",
                        "users": room_users,
                        "new_host": new_host["username"],
                    },
                    to=room_id,
                )
            elif len(room_users) == 0:
                # Remove room from database
                self.on_close_room(data)
                emit(
                    "leave_event",
                    {
                        "success": True,
                        "message": f"{user_name} has left the room {room_id}. No one left in the room.",
                        "users": room_users,
                        "new_host": "",
                    },
                    to=room_id,
                )
        except Exception as e:
            logger.info(e)
            emit(
                "leave_event",
                {
                    "success": False,
                    "message": f"Something went wrong, unable to leave due to {e}.",
                },
                to=room_id,
            )

    def on_close_room(self, data):
        room_id = data["room_id"]
        close_room(room_id)

        try:
            # Remove room from database
            num_of_rooms_closed = app.database.remove_room_data(room_id=room_id)

            # Send message to all users in room
            emit(
                "close_room_event",
                {
                    "success": True,
                    "message": f"Room {room_id} has been closed. Number of rooms closed is {num_of_rooms_closed}.",
                },
                broadcast=True,
            )
        except Exception as e:
            logger.info(e)
            emit(
                "close_room_event",
                {
                    "success": False,
                    "message": f"Something went wrong, unable to close room due to {e}.",
                },
                broadcast=True,
            )

    def on_start_room(self, data):
        room_activity = data["room_activity"]
        room_location = data["room_location"]
        room_id = data["room_id"]

        try:
            app.database.start_room(
                room_id=room_id,
                room_location=room_location,
                room_activity=room_activity,
                requesting_user_id=request.sid,
            )
            # Send message to all users in room
            emit(
                "start_room_event",
                {"success": True, "message": f"Room {room_id} has started."},
                broadcast=True,
            )
        except Exception as e:
            logger.info(e)
            emit(
                "start_room_event",
                {
                    "success": False,
                    "message": f"Something went wrong, unable to start room {room_id} due to {e}.",
                },
                broadcast=True,
            )

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
            emit(
                "kick_user_event",
                {
                    "success": True,
                    "message": f"{kick_user_name} has been kicked by the host",
                },
                to=room_id,
            )
        except Exception as e:
            logger.info(e)
            emit(
                "kick_user_event",
                {
                    "success": False,
                    "message": f"Something went wrong, unable to kick {kick_user_name} due to {e}.",
                },
                to=room_id,
            )

    def on_vote_option(self, data):
        room_id = data["room_id"]
        question_id = data["question_id"]
        option_id = data["option_id"]
        user_name = data["user_name"]

        try:
            num_of_votes = app.database.increment_vote(
                room_id=room_id, question_id=question_id, option_id=option_id
            )

            emit(
                "vote_option_event",
                {
                    "success": True,
                    "message": f"{user_name} has voted {option_id} for {question_id}. "
                    f"The number of votes for {question_id}, {option_id} is {num_of_votes}.",
                },
                to=room_id,
            )
        except Exception as e:
            logger.info(e)
            emit(
                "vote_option_event",
                {
                    "success": False,
                    "message": f"{user_name} cant vote {option_id} for {question_id}, due to {e}.",
                },
                to=room_id,
            )

    def on_start_round(self, data):
        room_id = data["room_id"]

        try:
            # get_reply() will handle storing questions and options into the database, as well as updating the time.
            reply, type_of_reply = app.llm.get_reply(
                room_id=room_id, database=app.database
            )
            reply["success"] = True
            # asking a question, we emit the question and options, then start the countdown
            if type_of_reply == "question":
                # reply = {"success": True
                #          "question_id": "123",
                #          "question_text": "What activity do you want to do?",
                #          "options": [{
                #                       "option_id": "1",
                #                       "option_text": "Hiking",
                #                       "votes": 0
                #                       }],
                #          }
                emit(
                    "start_round_event", reply, namespace="/room-management", to=room_id
                )

                # starts the countdown
                @copy_current_request_context
                def countdown_round():
                    sleep(Config.TIMER)
                    with app.app_context():
                        emit(
                            "end_round_event",
                            {"success": True, "message": f"Round ended for {room_id}."},
                            namespace="/room-management",
                        )

                countdown_thread = threading.Thread(target=countdown_round)
                countdown_thread.start()

            # giving the choice of activities, we just emit it instead.
            else:
                # reply = {"success": True,
                #          'activities': [{'activity_id': '1', 'activity_text': 'Escape Room Challenge at Lost SG'},
                #                         {'activity_id': '2', 'activity_text': 'Virtual Reality Experience at V-Room'}
                #                         ],
                #          'num_of_activity': 2}
                emit(
                    "start_round_event", reply, namespace="/room-management", to=room_id
                )
        except Exception as e:
            logger.info(e)
            emit(
                "start_round_event",
                {"success": False, "message": f"Unable to start a round due to {e}."},
                namespace="/room-management",
                to=room_id,
            )

    def on_set_room_properties(self, data):
        room_activity = data["room_activity"]
        room_location = data["room_location"]
        room_id = data["room_id"]

        try:
            emit(
                "set_room_properties_event",
                {
                    "success": True,
                    "message": f"Room {room_id} has set the activity to {room_activity} and "
                    f"location to {room_location}.",
                },
                to=room_id,
            )
        except Exception as e:
            logger.info(e)
            emit(
                "set_room_properties_event",
                {"success": False, "message": f"Something went wrong, due to {e}."},
                to=room_id,
            )
