from card import Card
from pack import Pack
from table import Table
from player import Player
from game import Game

from flask import request
from flask_socketio import emit
from app import app, game, socketio 

from auth import grant_token, check_token 
from serialization import send_data
from utils import refresh_data, send_error_message, send_info_message, send_message_to_everyone


@socketio.on("startDataRequest")
def start_data_request():
    socketio.emit("startData", {"playersNum": game.players_num(), "started": game.started()})

@socketio.on("join")
def join(data):
    if not game.started():
        nickname = data["nickname"]
        return_code = game.append_player(nickname, 100, request.sid)

        if return_code == 2:
            send_error_message("Nick musi mieć długość co najmniej 1 oraz może składać się wyłącznie z znaków a-z, 0-9, _", request.sid)
        elif return_code == 3:
            send_error_message("Gracz o takim nicku już istnieje", request.sid)
        else : 
            socketio.emit("joined", {"token": grant_token()}, to=request.sid)
            socketio.emit("startData", {"players_num": game.players_num(), "started": game.started()})
            refresh_data()
    else:
        send_error_message("Nie możesz dołączyć w trakcie trwającej rozgrywki", request.sid)


@socketio.on("startGame")
def start_game():
    if game.sid_to_player[request.sid] == 0:
        game.start()
        refresh_data()
        socketio.emit("startData", {"players_num": game.players_num(), "started": game.started()})


@socketio.on("gameDataRequest")
def game_data_request():
    send_data(request.sid)

@socketio.on("check")
def check():
    print("check")
    
    if game.check(request.sid) == 2:
        send_error_message("Serwer odmówił wykonania tej akcji", request.sid)
    else:
        refresh_data()

@socketio.on("bet")
def bet(data):
    amount = data["amount"]
    amount = str(amount)
    amount = int(amount)
    print("bet: ", amount)

    if game.make_bet(request.sid, amount) == 2:
        send_error_message("Serwer odmówił wykonania tej akcji", request.sid)
    else:
        refresh_data()

@socketio.on("call")
def call():
    print("call")
    
    if game.call(request.sid) == 2:
        send_error_message("Serwer odmówił wykonania tej akcji", request.sid)
    else:
        refresh_data()

@socketio.on("raise")
def raise_bet(data):
    amount = data["amount"]
    amount = str(amount)
    amount = int(amount)
    print("raise: ", amount)

    if game.raiseBet(request.sid, amount) == 2:
        send_error_message("Serwer odmówił wykonania tej akcji", request.sid)
    else:
        refresh_data()

@socketio.on("fold")
def fold():
    print("fold")

    if game.fold(request.sid) == 2:
        send_error_message("Serwer odmówił wykonania tej akcji", request.sid)
    else:
        refresh_data()

@socketio.on("allin")
def allin():
    print("allin")

    if game.allin(request.sid) == 2:
        send_error_message("Serwer odmówił wykonania tej akcji", request.sid)
    else:
        refresh_data()

@socketio.on("winners")
def winners(data):
    winnersNum = len(data)
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