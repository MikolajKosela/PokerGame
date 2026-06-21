from card import Card
from pack import Pack
from table import Table
from player import Player
from game import Game

from flask_socketio import emit
from app import app, game, socketio 

from serialization import send_data

def refresh_data():
    print("  Wyświetlam graczy, którym odświeżam dane")
    for player in game.players:
        print(player.nickname)
        send_data(player.sid)

def send_error_message(content, sid):
    socketio.emit("message", {"content": content, "style": "err"}, to=sid)

def send_info_message(content, sid):
    socketio.emit("message", {"content": content, "style": "info"}, to=sid)



