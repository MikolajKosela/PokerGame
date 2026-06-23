from game import Game

from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
game = Game()
socketio = SocketIO(app)

from routes.routes import *
from handlers.handlers import *

if __name__ == "__main__":
    socketio.run(app, debug=True)
