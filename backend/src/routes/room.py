from backend.src.routes import room_blueprint
from backend.src.utils.room import create_room_func
from flask import jsonify, request


@room_blueprint.route("/rooms", methods=["POST"])
def create_room():
    """
    An entry will be created in the database for the created room. A room code will
    be generated for the room. Set last_activity time in room.
    :return: JSON object
    """
    data = request.get_json()
    # db = current_app.database
    return jsonify(create_room_func(data["roomid"])), 200
    # data = request.get_json()
    # timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    # room_code = sha1(timestamp.encode("utf-8")).hexdigest()
    # room_id = uuid.uuid4().hex
    # room_json = {
    #     "roomid": room_id,
    #     "roomcode": room_code,
    #     "hostid": data['Userid'],
    #     "numuser": 30,
    #     "current_user": 1,
    #     "status": "Waiting",
    #     "last_activity": timestamp,
    #     "roomlocation": data['Location'],
    #     "roomactivity": data['Activity'],
    #     "users": [{
    #         "userid": data['Userid'],
    #         "username": data['Username']
    #     }],
    #     "questions": []
    # }
    # success = redis_database.store(room_id, room_code, room_json)
    # if success:
    #     information = {
    #         "Success": True,
    #         "Room code": room_code,
    #         "Room id": room_id
    #     }
    #     return jsonify(information), 200
    # else:
    #     return "Internal Server Error", 200


@room_blueprint.route("/rooms/<roomid>", methods=["POST"])
def delete_room(roomid):
    """
    Remove the database entry for the room. Entries in the database
    for the room’s users, questions, votes, and options will be removed.
    :return: None
    """
    # success = redis_database.remove(roomid)
    # if success:
    #     return jsonify({
    #         "Success": success
    #     }), 200
    # else:
    #     return "Internal server error", 500


@room_blueprint.route("/rooms", methods=["GET"])
def get_room_id():
    """
    Finds the roomid corresponding to the room code. If room does not exist, return False.
    :return: None
    """
    return "Success", 200


@room_blueprint.route("/rooms/<roomid>/users", methods=["POST"])
def join_room(roomid):
    """
    Checks the num_users, and adds user to users table if number is < capacity.
    Increment num_users by 1 and set last_activity time in room.
    :return: None
    """
    # room_json = redis_database.query(roomid)
    # if room_json is not None:
    #     pass
    # else:
    #     pass
    # timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    #
    # return "Success",200


@room_blueprint.route("/rooms/<roomid>/users/<userid>", methods=["DELETE"])
def leave_room(roomid, userid):
    """
    A user clicks “leave room”. Remove user from database and reduce num_users by 1.
    :return: None
    """
    # room = redis_database.query(roomid)
    # room['current_num_users'] -= 1
    #
    # return "Success", 200
