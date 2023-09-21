import os
from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS

from src.database.Database import Database
from src.routes.Room import room_blueprint
from src.routes.User import user_blueprint
from src.routes.Chatgpt import chatgpt_blueprint

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

    app.database = database

    app.register_blueprint(room_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(chatgpt_blueprint)

    from src.sockets.room_management import RoomManagement

    socketio.on_namespace(RoomManagement("/room-management"))
    socketio.init_app(app)
    return app
