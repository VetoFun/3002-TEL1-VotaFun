from flask import Flask
import os
from flask_cors import CORS

from src.database.Database import Database

from src.routes.Room import room_blueprint
from src.routes.User import user_blueprint
from src.routes.Chatgpt import chatgpt_blueprint


def create_app():
    app = Flask(__name__)
    app_settings = os.environ.get("APP_SETTINGS", "src.config.DevelopmentConfig")
    app.config.from_object(app_settings)
    print(f"redis url: {app.config['REDIS_URL']}")
    CORS(app, supports_credentials=True)
    app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "")

    database = Database(
        redis_url=app.config["REDIS_URL"],
        redis_host=app.config["REDIS_HOST"],
        redis_port=app.config["REDIS_PORT"],
    )

    app.database = database

    app.register_blueprint(room_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(chatgpt_blueprint)

    return app


if __name__ == "__main__":
    create_app().run()  # use flask run --debug --port=<your port>
