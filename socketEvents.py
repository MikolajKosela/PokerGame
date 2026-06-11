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
from app import *

socketio = SocketIO(app)

def grantToken():
    id = random.randint(1000, 100000)
    while id in game.idToPlayer.keys():
        id = random.randint(1000, 100000)

    game.idToPlayer[id] = len(game.idToPlayer)
    return id

def checkToken(token):
    token = str(token)
    if token.isdecimal() == False:
        return False

    token = int(token)

    print(game.idToPlayer)
    if token in game.idToPlayer.keys():
        return True
    return False 


@socketio.on("handshake")
def handshake(data):
    ok = False
    print(data)
    if checkToken(data["token"]) == True:
        ok = True

    if ok == True:
        curID = game.idToPlayer[int(data["token"])]
        session["ID"] = curID
        session["nickname"] = game.players[curID].nickname
        print(session)

    socketio.emit("handshakeAnswer", {"ok" : ok}, to=request.sid)

@socketio.on("checkStateRequest")
def checkState():
    nickname = session.get("nickname")
    curID = session.get("ID")
    playerExist = False

    state = 0
    # 0 - start
    # 1 - lobby
    # 2 - action
    # 3 - wait
    # 4 - end

    if curID == None:
        state = "/"
    elif game.isEnd == True:
        state = "/end"
    elif game.whoseRoundIs == -1:
        state = "/lobby"
    elif curID == game.whoseRoundIs:
        state = "/action"
    elif curID != game.whoseRoundIs:
        state = "/wait"

    print("Dostałem zapytanie, wysyłam", state)
    socketio.emit("checkState", {"state": state}, to=request.sid)


@socketio.on("join")
def join(data):
    state = checkState()
    if state is not None:
        return state

    nickname = data["nickname"]
    session["nickname"] = nickname
    session["ID"] = len(game.players)
    game.players.append(Player(nickname, 99, len(game.players)))
    game.playersNum = len(game.players)

    socketio.emit("joined", {"token": grantToken()}, to=request.sid)

@socketio.on("lobbyRequest")
def lobby():
    playersNum = game.playersNum
    admin = game.players[0].nickname
    socketio.emit("lobby", {
        "playersNum" : playersNum, 
        "admin" : admin
        })
