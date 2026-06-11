from card import Card
from pack import Pack
from table import Table
from player import Player
from game import Game
from flask import (
    Flask,
    request,
    render_template,
    url_for,
    redirect,
    jsonify,
    session,
)
from flask_socketio import SocketIO, emit
import random

app = Flask(__name__)
app.secret_key = "tajny klucz"
game = Game()

from routes import *
from socketEvents import *

if __name__ == "__main__":
    app.run(debug=True)
