from src.routes import chatgpt_blueprint
from flask import request, current_app

from src.utils.Chatgpt import chatgpt_func


@chatgpt_blueprint.route("/chatgpt", methods=["POST"])
def chatgpt_route():
    """
    Route to handle post request to "/chatgpt".
    :return: response code 200 if the operation succeed, otherwise response code 500 is returned
    """
    data = request.get_json()
    database = current_app.database
    try:
        result = chatgpt_func(data, database)
        if "error" in result:
            return result, 500
        else:
            return result, 200
    except Exception:
        return {"success": False, "error": "Internal Server Error"}, 500
