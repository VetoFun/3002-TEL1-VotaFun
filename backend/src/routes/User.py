from backend.src.routes import user_blueprint
from backend.src.utils.User import get_all_users_func, change_host_func
from flask import current_app, jsonify, request


@user_blueprint.route("/rooms/<room_id>/users", methods=["GET"])
def get_all_users(room_id: str):
    """
    :param room_id:
    :return:
    """
    database = current_app.database
    results = get_all_users_func(room_id, database)

    if "error" in results:
        return jsonify(results), 500
    else:
        return jsonify(results), 200


@user_blueprint.route("/rooms/<room_id>/changehost", methods=["PUT"])
def change_host(room_id: str):
    """

    :param room_id:
    :return:
    """
    data = request.get_json()
    database = current_app.database
    results = change_host_func(room_id, data["new_hostid"], database)

    if "error" in results:
        return jsonify(results), 500
    else:
        return jsonify(results), 200
