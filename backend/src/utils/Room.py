from src.database import Database
from src.database.Room import Room
from src.database import User
from datetime import datetime
from hashlib import sha1

from src.logger import logger


def create_room_func(data: dict, database: Database):
    """
    Creates an entry in the database for the new room, with status == WAITING. A unique room id will be generated
    and returned.
    :param data: Request body.
    :param database: Application database.
    :return: success == True and room_id if the room is created and stored. Otherwise, raise an exception.
    """
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    room_id = sha1(timestamp.encode("utf-8")).hexdigest()
    try:
        # creates host user and room
        room = Room(
            room_id,
            1,
            30,
            timestamp,
            [],
            "",
            "",
            "",
            "",
            [],
        )
        # add to database
        database.store_room_data(room_id, room)
        return {"success": True, "room_id": room_id}
    except Exception:
        raise


def delete_room_func(room_id: str, database: Database):
    """
    Deletes the room from the database. All information will be removed.
    :param room_id: Room id of the room to be removed.
    :param database: Application database.
    :return: success == True and room_id if the room is deleted. Otherwise, raise an exception.
    """
    try:
        room_deleted = database.remove_room_data(room_id)
        if room_deleted == 1:
            return {"success": True}
        else:
            return {"success": False, "error": "Internal Server Error"}
    except Exception:
        raise


# def get_room_id_func(roomid: str, database: Database):
#     """
#     :param room_id:
#     :param database:
#     :return:
#     """
#     pass


def join_room_func(room_id: str, data: dict, database: Database):
    """
    Adds a user to the room. If the number of user exceeds max capacity (30), then they will not be added.
    :param room_id: Room id of the room the user is joining.
    :param data: Request body.
    :param database: Application database.
    :return: success == True if the user is added. success == False if the room exceeds max capacity.
    Otherwise, raise an exception.
    """

    try:
        room = database.query_room_data(room_id, False)
    except KeyError:
        raise

    num_user = room.get_number_of_user()
    max_capacity = room.get_max_capacity()

    if num_user + 1 > max_capacity:
        return {"success": False, "error": "Number of user is at max capacity"}
    else:
        user = User(data["username"], data["user_id"])
        room.add_user(user)
        database.store_room_data(room_id, room)
        return {"success": True}


def leave_room_func(room_id: str, user_id: str, database: Database):
    """
    Removes a user from a room.
    :param room_id: Room id of the room that the user left.
    :param user_id: User id of the user that left.
    :param database: Application database.
    :return: success == True if the user is removed, and the number of users and if the user that left is
    the host is returned. Otherwise, raise an exception.
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
        raise
