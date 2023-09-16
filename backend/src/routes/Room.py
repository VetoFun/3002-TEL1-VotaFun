from backend.src.routes import room_blueprint
from backend.src.utils.Room import create_room_func, delete_room_func, join_room_func
from flask import jsonify, request, current_app


@room_blueprint.route("/createroom", methods=["POST"])
def create_room():
    """
    An entry will be created in the database for the created room. A room code will
    be generated for the room. Set last_activity time in room.
    :return: JSON object
    """
    data = request.get_json()
    database = current_app.database
    result = create_room_func(data, database)

    if result["success"]:
        return jsonify(result), 200
    else:
        return jsonify(result), 500


@room_blueprint.route("/closeroom/<room_id>", methods=["POST"])
def delete_room(room_id: str):
    """
    Remove the database entry for the room. Entries in the database
    for the room’s users, questions, votes, and options will be removed.
    :return: None
    """
    database = current_app.database
    result = delete_room_func(room_id, database)

    if result["success"]:
        return jsonify(result), 200
    else:
        return jsonify(result), 500


# @room_blueprint.route("/rooms", methods=["GET"])
# def get_room_id(room_id: str):
#     """
#     Finds the roomid corresponding to the room code. If room does not exist, return False.
#     :return: None
#     """
#     database = current_app.database
#     result = get_room_id_func(room_id, database)
#     return "Success", 200


@room_blueprint.route("/joinroom/<room_id>/users", methods=["POST"])
def join_room(room_id: str):
    """
    Checks the num_users, and adds user to users table if number is < capacity.
    Increment num_users by 1 and set last_activity time in room.
    :return: None
    """
    data = request.get_json()
    database = current_app.database
    result = join_room_func(room_id, data, database)

    if "error" not in result:
        return jsonify(result), 200
    else:
        return jsonify(result), 500


@room_blueprint.route("/rooms/<room_id>/users/<user_id>", methods=["DELETE"])
def leave_room(room_id, user_id):
    """
    :param room_id:
    :param user_id:
    :return:
    """
    # room = redis_database.query(roomid)
    # room['current_num_users'] -= 1
    #
    # return "Success", 200
