from src.routes import room_blueprint
from src.utils.Room import (
    create_room_func,
    delete_room_func,
    join_room_func,
    leave_room_func,
)
from src.logger import logger
from flask import jsonify, request, current_app


@room_blueprint.route("/createroom", methods=["POST"])
def create_room_route():
    """
    Route to handle post request to "/createroom".
    :return: response code 200 if the operation succeed, otherwise response code 500 is returned.
    """
    data = request.get_json()
    database = current_app.database
    try:
        result = create_room_func(data, database)
        return jsonify(result), 200
    except Exception as e:
        logger.error(e)
        return {"success": False, "error": "Internal Server Error"}, 500


@room_blueprint.route("/closeroom/<room_id>", methods=["DELETE"])
def delete_room_route(room_id: str):
    """
    Route to handle delete request to "/closeroom/<room_id>".
    :param room_id: Room id to be deleted.
    :return: response code 200 if the operation succeed, otherwise response code 500 is returned.
    """
    database = current_app.database
    try:
        result = delete_room_func(room_id, database)
        return jsonify(result), 200
    except Exception:
        return {"success": False, "error": "Internal Server Error"}, 500


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
def join_room_route(room_id: str):
    """
    Route to handle post request to "/joinroom/<room_id>/users".
    :param room_id: Room id of the room that the user joined.
    :return: response code 200 if the operation succeed, otherwise response code 500 is returned.
    """
    data = request.get_json()
    database = current_app.database
    try:
        result = join_room_func(room_id, data, database)
        return jsonify(result), 200
    except Exception as e:
        logger.error(e)
        return {"success": False, "error": "Internal Server Error"}, 500


@room_blueprint.route("/leaveroom/<room_id>/users/<user_id>", methods=["DELETE"])
def leave_room_route(room_id: str, user_id: str):
    """
    Route to handle delete request to "/leaveroom/<room_id>/users/<user_id>".
    :param room_id: Room id of the room that the user left.
    :param user_id: User id of the user that left the room.
    :return: response code 200 if the operation succeed, otherwise response code 500 is returned.
    """
    database = current_app.database
    try:
        result = leave_room_func(room_id, user_id, database)
        return jsonify(result), 200
    except Exception:
        return {"success": False, "error": "Internal Server Error"}, 500
