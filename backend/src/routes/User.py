from src.routes import user_blueprint
from src.utils.User import get_all_users_func, change_host_func
from flask import current_app, jsonify, request


@user_blueprint.route("/rooms/<room_id>/getusers", methods=["GET"])
def get_all_users_route(room_id: str):
    """
    Route to handle get request to "/rooms/<room_id>/getusers".
    :param room_id: Room id to get all the users from.
    :return: response code 200 if the operation succeed, otherwise response code 500 is returned.
    """
    database = current_app.database
    try:
        results = get_all_users_func(room_id=room_id, database=database)
        return jsonify(results), 200
    except Exception:
        # todo: log exception
        return {"success": False, "error": "Internal Server Error"}, 500


@user_blueprint.route("/rooms/<room_id>/changehost", methods=["PUT"])
def change_host_route(room_id: str):
    """
    Route to handle put request to "/rooms/<room_id>/changehost".
    :param room_id: Room id to change host.
    :return: response code 200 if the operation succeed, otherwise response code 500 is returned.
    """
    data = request.get_json()
    database = current_app.database

    try:
        results = change_host_func(
            room_id=room_id, new_hostid=data["new_hostid"], database=database
        )
        return jsonify(results), 200
    except Exception:
        return {"success": False, "error": "Internal Server Error"}, 500
