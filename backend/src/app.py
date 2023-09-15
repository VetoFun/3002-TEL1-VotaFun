import os

from flask import Flask
from flask_cors import CORS

from .database.Database import Database


app = Flask(__name__)
app_settings = os.environ.gett("APP_SETTINGS", "src.config.DevelopmentConfig")
app.config.from_object(app_settings)
CORS(app, supports_credentials=True)

redis_db = Database(
    redis_url=app.config["REDIS_URL"],
    redis_host=app.config["REDIS_HOST"],
    redis_port=app.config["REDIS_PORT"],
)


if __name__ == "__main__":
    app.run()
