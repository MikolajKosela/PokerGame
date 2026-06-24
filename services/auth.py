from models import Card, Pack, Table, Player 
from game import Game

from flask import request
from flask_socketio import emit
from app import app, game, socketio 

from secrets import token_urlsafe

@socketio.on("handshake")
def handshake(data):
    playerID = check_token(data["token"]) 

    if playerID == None:
        return socketio.emit("handshakeAnswer", {"ok" : False}, to=request.sid)

    game.sid_to_player[request.sid] = playerID 

    if playerID >= 0 and playerID < len(game.players):
        game.players[playerID].sid = request.sid

        return socketio.emit("handshakeAnswer", {"ok" : True, "admin" : playerID == game.adminID}, to=request.sid)

    return socketio.emit("handshakeAnswer", {"ok" : False}, to=request.sid)


def grant_token():
    token = token_urlsafe(32)
    while token in game.sid_to_player.keys():
        token = token_urlsafe(32)

    game.token_to_player[str(token)] = len(game.sid_to_player)
    return token

def check_token(token):
    token = str(token)

    if token in game.token_to_player.keys():
        return game.token_to_player[token]
    return None 