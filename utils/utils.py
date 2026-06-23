from models import Card, Pack, Table, Player
from game import Game

from flask_socketio import emit
from app import app, game, socketio 

from services.serialization import send_data, send_logs

def refresh_data():
    print("  Wyświetlam graczy, którym odświeżam dane")
    send_logs()
    for player in game.players:
        print(player.nickname)
        send_data(player.sid)

def send_error_message(content, sid):
    socketio.emit("message", {"content": content, "style": "err"}, to=sid)

def send_info_message(content, sid):
    socketio.emit("message", {"content": content, "style": "info"}, to=sid)

def send_message_to_everyone(content):
    socketio.emit("message", {"content": content, "style": None})



