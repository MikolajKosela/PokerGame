from models import Card, Pack, Table, Player 
from game import Game

from flask import request
from flask_socketio import emit
from app import app, game, socketio 

import random

@socketio.on("handshake")
def handshake(data):
    ok = False
    print(data)
    if check_token(data["token"]) == True:
        ok = True

    admin = False

    if ok == True:
        cur_ID = game.token_to_player[int(data["token"])]
        game.sid_to_player[request.sid] = cur_ID
        if cur_ID >= 0:
            game.players[cur_ID].sid = request.sid
        if cur_ID == game.adminID:
            admin = True

    socketio.emit("handshakeAnswer", {"ok" : ok, "admin" : admin}, to=request.sid)

def grant_token():
    token = random.randint(1000, 100000)
    while token in game.sid_to_player.keys():
        token = random.randint(1000, 100000)

    game.token_to_player[token] = len(game.sid_to_player)
    return token

def check_token(token):
    token = str(token)
    if token.isdecimal() == False:
        return False

    token = int(token)

    if token in game.token_to_player.keys():
        return True
    return False 