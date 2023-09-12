from flask import Flask
from redisdb.src.Database import Database

app = Flask(__name__)
# database setup
redis_database = Database()

if __name__ == "__main__":
    app.run(debug=True)
