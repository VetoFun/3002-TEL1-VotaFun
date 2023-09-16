from src.database import Database
from src.database.Room import Room
from src.database import User
from datetime import datetime
from hashlib import sha1

from src.logger import logger


def create_room_func(data: dict, database: Database):
    """
    Creates a Room object, and stores it in the database.
    :param data: Request Body
    :param database: Database instance
    :return: success = True and room_id if the room is created and stored. None if the room was not stored.
    """
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    room_id = sha1(timestamp.encode("utf-8")).hexdigest()
    try:
        # creates host user and room
        user = User(data["username"], data["host_id"])
        room = Room(
            room_id,
            1,
            30,
            timestamp,
            [],
            data["host_id"],
            "",
            data["location"],
            data["activity"],
            [user],
        )
        # add to database
        database.store_room_data(room_id, room)
        return {"success": True, "room_id": room_id}
    except Exception:
        return {"success": False, "error": "Internal Server Error"}


def delete_room_func(room_id: str, database: Database):
    """
    :param room_id:
    :param database:
    :return:
    """
    try:
        room_deleted = database.remove_room_data(room_id)
        if room_deleted == 1:
            return {"success": True}
    except Exception:
        return {"success": False, "error": "Internal Server Error"}


# def get_room_id_func(roomid: str, database: Database):
#     """
#     :param room_id:
#     :param database:
#     :return:
#     """
#     pass


def join_room_func(room_id: str, data: dict, database: Database):
    """
    :param room_id:
    :param data:
    :param database:
    :return:
    """

    try:
        room = database.query_room_data(room_id, False)
    except KeyError:
        return {"success": False, "error": "Internal Server Error"}

    num_user = room.get_number_of_user()
    max_capacity = room.get_max_capacity()

    if num_user + 1 > max_capacity:
        return {"success": False, "error": "Number of user is at max capacity."}
    else:
        user = User(data["username"], data["user_id"])
        room.add_user(user)
        database.store_room_data(room_id, room)
        return {"success": True}


def leave_room_func(room_id: str, user_id: str, database: Database):
    """
    :param room_id:
    :param user_id:
    :param database:
    :return:
    """
    try:
        room = database.query_room_data(room_id)
        num_user = database.remove_user(room_id, user_id)
        logger.info(f"Number of user in {room_id} is {num_user}.")
        return {
            "success": True,
            "num_users": num_user,
            "is_host": room["host_id"] == user_id,
        }
    except Exception:
        return {"success": False, "error": "Internal Server Error"}
