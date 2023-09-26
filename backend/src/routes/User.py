from flask import current_app, jsonify, request

from src.routes import user_blueprint
from src.logger import logger


@user_blueprint.route("/rooms/<room_id>/getusers", methods=["GET"])
def get_all_users_route(room_id: str):
    """
    Route to handle get request to "/rooms/<room_id>/getusers".
    :param room_id: Room id to get all the users from.
    :return: response code 200 if the operation succeed, otherwise response code 500 is returned.
    """
    try:
        results = {
            "success": True,
            "users": current_app.database.get_users(room_id=room_id),
        }
        return jsonify(results), 200
    except Exception as e:
        logger.error(e)
        return {"success": False, "error": "Internal Server Error"}, 500


@user_blueprint.route("/rooms/<room_id>/changehost", methods=["PUT"])
def change_host_route(room_id: str):
    """
    Route to handle put request to "/rooms/<room_id>/changehost".
    :param room_id: Room id to change host.
    :return: response code 200 if the operation succeed, otherwise response code 500 is returned.
    """
    data = request.get_json()

    try:
        current_app.database.change_host(
            room_id=room_id, new_host_id=data.get("new_hostid")
        )
        return jsonify({"success": True}), 200
    except Exception as e:
        logger.error(e)
        return {"success": False, "error": "Internal Server Error"}, 500
