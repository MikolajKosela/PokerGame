from game import Game
from routes.routes import register_routes
from handlers.handlers import register_handlers

from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
game = Game()
socketio = SocketIO(app)

register_routes(app)
register_handlers(socketio, game)

if __name__ == "__main__":
    socketio.run(app, debug=True)
