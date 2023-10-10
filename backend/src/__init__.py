import os
from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS

from src.database.Database import Database
from src.utils.LLM import LLM

socketio = SocketIO(cors_allowed_origins="*")


def create_app():
    app = Flask(__name__)
    app_settings = os.environ.get("APP_SETTINGS", "src.config.DevelopmentConfig")
    app.config.from_object(app_settings)
    app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "")

    CORS(app, supports_credentials=True)
    database = Database(
        redis_url=app.config["REDIS_URL"],
        redis_host=app.config["REDIS_HOST"],
        redis_port=app.config["REDIS_PORT"],
    )
    llm = LLM()

    app.llm = llm
    app.database = database

    from src.sockets.RoomManagement import RoomManagement

    socketio.on_namespace(RoomManagement("/room-management"))
    socketio.init_app(app)
    return app
