from src.routes import room_blueprint
from src.logger import logger
from flask import jsonify, request, current_app
import traceback


@room_blueprint.route("/createroom", methods=["POST"])
def create_room_route():
    """
    Route to handle post request to "/createroom".
    :return: response code 200 if the operation succeed, otherwise response code 500 is returned.
    """
    try:
        result = {
            "success": True,
            "room_id": current_app.database.create_room(),
        }
        return jsonify(result), 200
    except Exception as e:
        print(traceback.format_exc())
        logger.error(e)
        return {"success": False, "error": "Internal Server Error"}, 500


@room_blueprint.route("/closeroom/<room_id>", methods=["DELETE"])
def delete_room_route(room_id: str):
    """
    Route to handle delete request to "/closeroom/<room_id>".
    :param room_id: Room id to be deleted.
    :return: response code 200 if the operation succeed, otherwise response code 500 is returned.
    """
    try:
        result = {
            "success": True,
            "num_deleted": current_app.database.remove_room_data(room_id=room_id),
        }
        return jsonify(result), 200
    except Exception as e:
        logger.error(e)
        return {"success": False, "error": "Internal Server Error"}, 500


@room_blueprint.route("/joinroom/<room_id>/users", methods=["POST"])
def join_room_route(room_id: str):
    """
    Route to handle post request to "/joinroom/<room_id>/users".
    :param room_id: Room id of the room that the user joined.
    :return: response code 200 if the operation succeed, otherwise response code 500 is returned.
    """
    data = request.get_json()
    user_id = data.get("user_id")
    username = data.get("username")
    try:
        result = {
            "success": True,
            "num_users": current_app.database.add_user(
                room_id=room_id, user_id=user_id, username=username
            ),
        }
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
    try:
        num_users, is_host = current_app.database.remove_user(
            room_id=room_id, user_id=user_id
        )
        result = {"success": True, "num_users": num_users, "is_host": is_host}
        return jsonify(result), 200
    except Exception as e:
        logger.error(e)
        return {"success": False, "error": "Internal Server Error"}, 500
