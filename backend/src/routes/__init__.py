from flask import Blueprint

chatgpt_blueprint = Blueprint("chatgpt", __name__)
room_blueprint = Blueprint("room", __name__)
user_blueprint = Blueprint("user", __name__)

from backend.src.routes.chatgpt import *  # noqa
from backend.src.routes.room import *  # noqa
from backend.src.routes.user import *  # noqa
