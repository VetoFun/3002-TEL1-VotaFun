from flask import Blueprint

chatgpt_blueprint = Blueprint("chatgpt", __name__)
room_blueprint = Blueprint("room", __name__)
user_blueprint = Blueprint("user", __name__)

from backend.src.routes.Chatgpt import *  # noqa
from backend.src.routes.Room import *  # noqa
from backend.src.routes.User import *  # noqa
