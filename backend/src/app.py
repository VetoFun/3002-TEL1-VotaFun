from flask import Flask
import os
from flask_cors import CORS

from .database.Database import Database

from backend.src.routes.chatgpt import chatgpt_blueprint
from backend.src.routes.room import room_blueprint
from backend.src.routes.user import user_blueprint


def create_app():
    app = Flask(__name__)
    app_settings = os.environ.get("APP_SETTINGS", "src.config.DevelopmentConfig")
    app.config.from_object(app_settings)
    CORS(app, supports_credentials=True)
    app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY")

    redis_db = Database(
        redis_url=app.config["REDIS_URL"],
        redis_host=app.config["REDIS_HOST"],
        redis_port=app.config["REDIS_PORT"],
    )

    app.redis_db = redis_db
    app.register_blueprint(chatgpt_blueprint)
    app.register_blueprint(room_blueprint)
    app.register_blueprint(user_blueprint)

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
