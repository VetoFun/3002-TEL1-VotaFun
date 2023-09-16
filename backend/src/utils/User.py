from src.database import Database


def get_all_users_func(room_id: str, database: Database):
    """

    :param room_id:
    :param database:
    :return:
    """
    try:
        users = database.get_users(room_id)
        return {"success": True, "users": users}
    except Exception:
        return {"success": False, "error": "Internal Server Error"}


def change_host_func(room_id: str, new_hostid: str, database: Database):
    """

    :param room_id:
    :param new_hostid:
    :param database:
    :return:
    """
    try:
        room = database.query_room_data(room_id, False)
        room.set_host(new_hostid)
        database.store_room_data(room_id, room)
        return {"success": True}
    except Exception:
        return {"success": False, "error": "Internal Server Error"}
