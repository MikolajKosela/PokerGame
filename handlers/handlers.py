from models import Card, Pack, Table, Player, Result
from game import Game

from flask import request
from flask_socketio import emit
from app import app, game, socketio 

from services.auth import grant_token, check_token 
from services.serialization import send_data
from utils.utils import refresh_data, send_error_message, send_info_message, send_message_to_everyone
from services.serialization import build_start_data

@socketio.on("startDataRequest")
def start_data_request():
    socketio.emit("startData", build_start_data())

@socketio.on("join")
def join(data):
    if not game.started():
        nickname = data["nickname"]
        return_code = game.append_player(nickname, 100, request.sid)

        if return_code.ok == True:
            socketio.emit("joined", {"token": grant_token()}, to=request.sid)
            refresh_data()
        else:
            send_error_message(return_code.info, request.sid)
    else:
        send_error_message("Nie możesz dołączyć w trakcie trwającej rozgrywki", request.sid)


@socketio.on("startGame")
def start_game():
    if game.sid_to_player[request.sid] == 0:
        game.start()
        refresh_data()

@socketio.on("gameDataRequest")
def game_data_request():
    send_data(request.sid)

@socketio.on("check")
def check():
    print("check")
    
    return_code = game.check(request.sid)

    if return_code == None:
        refresh_data()
    else:
        send_error_message(return_code.info, request.sid)

@socketio.on("bet")
def bet(data):
    amount = int(data["amount"])
    print("bet: ", amount)

    return_code = game.make_bet(request.sid, amount)

    if return_code == None:
        refresh_data()
    else:
        send_error_message(return_code.info, request.sid)

@socketio.on("call")
def call():
    print("call")
    
    return_code = game.call(request.sid)

    if return_code == None:
        refresh_data()
    else:
        send_error_message(return_code.info, request.sid)

@socketio.on("raise")
def raise_bet(data):
    amount = int(data["amount"])
    print("raise: ", amount)

    return_code = game.raiseBet(request.sid, amount)

    if return_code == None:
        refresh_data()
    else:
        send_error_message(return_code.info, request.sid)

@socketio.on("fold")
def fold():
    print("fold")

    return_code = game.fold(request.sid)

    if return_code == None:
        refresh_data()
    else:
        send_error_message(return_code.info, request.sid)

@socketio.on("allin")
def allin():
    print("allin")

    return_code = game.allin(request.sid)

    if return_code == None:
        refresh_data()
    else:
        send_error_message(return_code.info, request.sid)

@socketio.on("winners")
def winners(data):
    winnersNum = len(data)
    if winnersNum != 0:
        for player in data:
            id = int(player)
            game.players[id].credits += game.pot // winnersNum
    
        game.pot %= winnersNum
    socketio.emit("creditsGranted")
    refresh_data()

@socketio.on("newDeal")
def newDeal():
    game.again()
    refresh_data()