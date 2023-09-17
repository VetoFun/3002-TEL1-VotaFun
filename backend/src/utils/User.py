from src.database import Database


def get_all_users_func(room_id: str, database: Database):
    """
    Gets all users in the room specified by the room id from the database.
    :param room_id: Room id of the room to get users from.
    :param database: Application database.
    :return: List of users, and success == True if the operation succeed, otherwise raise an exception.
    """
    try:
        users = database.get_users(room_id)
        return {"success": True, "users": users}
    except Exception:
        raise


def change_host_func(room_id: str, new_hostid: str, database: Database):
    """
    Changes the room host, and stores the information into the database.
    :param room_id: Room id to change host.
    :param new_hostid: New host id to change to.
    :param database:Application database.
    :return: Success == True if the operation succeed, otherwise raise an exception.
    """
    try:
        room = database.query_room_data(room_id, False)
        room.set_host(new_hostid)
        database.store_room_data(room_id, room)
        return {"success": True}
    except Exception:
        raise
