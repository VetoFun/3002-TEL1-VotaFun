from . import create_app, socketio

if __name__ == "__main__":
    app = create_app()
    socketio.run(app, port=5001, debug=True)  # use flask run --debug --port=<your port>
