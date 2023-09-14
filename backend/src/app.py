from flask import Flask
import os

from backend.src.routes.chatgpt import chatgpt_blueprint
from backend.src.routes.room import room_blueprint
from backend.src.routes.user import user_blueprint

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY")

app.register_blueprint(chatgpt_blueprint)
app.register_blueprint(room_blueprint)
app.register_blueprint(user_blueprint)

if __name__ == "__main__":
    app.run(debug=True)
