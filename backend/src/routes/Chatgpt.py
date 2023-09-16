from backend.src.routes import chatgpt_blueprint
from flask import request, current_app

from backend.src.utils.Chatgpt import chatgpt_func


@chatgpt_blueprint.route("/chatgpt", methods=["POST"])
def chatgpt():
    # Todo: Ensure that the correct status code is returned.
    """
    API which is a wrapper to call openai API. This fetches all the questions and votes so far, then uses openai
    ChatCompletion to get a reply from ChatGPT.
    :return:
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
        return {"success": False, "error": "Internal Server Error"}
