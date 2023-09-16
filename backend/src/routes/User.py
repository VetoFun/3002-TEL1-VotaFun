from backend.src.routes import user_blueprint


@user_blueprint.route("/rooms/<roomid>/users", methods=["GET"])
def get_all_users(roomid):
    """
    Get all users in a room
    :return: None
    """


@user_blueprint.route("/rooms/<roomid>/changehost", methods=["PUT"])
def change_host():
    """
    Changes the host into another user.
    :return: None
    """
