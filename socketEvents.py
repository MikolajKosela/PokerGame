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
)
from flask_socketio import SocketIO, emit
import random
from app import *

socketio = SocketIO(app)

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

def summary():
    if game.is_end() == False:
        return False
    sumarry_data = []
    for i, player in enumerate(game.players):
        cards = [card.to_dict() for card in game.tables[i].cards]
        sumarry_data.append(
            {
                "nickname": player.nickname,
                "id": player.ID,
                "fold": player.fold,
                "credits": player.credits,
                "cards": cards,
            }
        )
    socketio.emit("summary", sumarry_data)

def check_state(sid):
    cur_ID = game.sid_to_player[sid]
    nickname = game.players[cur_ID].nickname

    state = "/"
    # 0 - start
    # 1 - lobby
    # 2 - action
    # 3 - wait
    # 4 - end
    print (cur_ID, game.is_end(), game.whose_round_is)

    if cur_ID == None:
        state = "/"
    elif game.is_end() == True:
        state = "/end"
    elif game.whose_round_is == -1:
        state = "/lobby"
    elif cur_ID == game.whose_round_is:
        state = "/action"
    elif cur_ID != game.whose_round_is:
        state = "/wait"

    print("Dostałem zapytanie od", cur_ID, nickname, "wysyłam", state)
    return state

def build_possible_moves(sid):
    player = game.players[game.sid_to_player[sid]]

    possibilities = {
        "check": player.can_check(game),
        "bet": player.can_bet(game),
        "call": player.can_call(game),
        "raise": player.can_raise(game),
        "fold": player.can_fold(game),
        "allin": player.can_allin(game),
    }
    return possibilities

def send_data(sid):
    print("Wysyłam dane do gracza: ", sid)
    state = "/"
    my_ID = None
    my_data = None
    cur_ID = None
    cur_nick = None
    players_num = None
    pot = None 
    bet = None 
    round_num = None
    your_bet = None
    your_credits = None 
    your_round_skipped = None

    common_cards = None 
    player_cards = None
    round_data = None 
    players = None 
    buttons = None 

    if game.sid_to_player.get(sid) != None:
        my_ID = game.sid_to_player[sid]
        state = check_state(sid)
        print(" ID GRACZA ", my_ID, game.players[my_ID].nickname)

    players_num = game.players_num()
    players = [player.to_dict() for player in game.players]

    if (game.whose_round_is >= 0 or game.is_end()) and my_ID != None:
        my_data = game.players[my_ID]
        common_cards = game.tables[-1].to_dict()
        player_cards = game.tables[my_ID].to_dict()

        cur_ID = game.whose_round_is
        if cur_ID >= 0:
            cur_nick = game.players[cur_ID].nickname

        pot = game.pot
        bet = game.bet - my_data.bet

        round_num = game.round_num
        your_bet = my_data.bet
        your_credits = my_data.credits
        your_round_skipped = my_data.last_round_skipped

        buttons = build_possible_moves(sid)

    round_data = {
        "curID": cur_ID,
        "curNick": cur_nick,
        "playersNum": players_num,
        "pot": pot, 
        "bet": bet,
        "roundNum": round_num,
        "yourBet": your_bet,
        "yourCredits": your_credits,
        "lastRoundSkipped": game.last_round_skipped,
        "yourRoundSkipped": your_round_skipped
    }
    
    data = {
        #"sid": sid,
        "state": state,
        "commonCards": common_cards,
        "playerCards": player_cards,
        "roundData": round_data,
        "buttons": buttons,
        "players": players
    }

    if game.is_end() == True:
        summary()
    socketio.emit("gameData", data, to=sid)

def refresh_data():
    print("  Wyświetlam graczy, którym odświeżam dane")
    for player in game.players:
        print(player.nickname)
        send_data(player.sid)

def send_error_message(content, sid):
    socketio.emit("message", {"content": content, "style": "err"}, to=sid)

def send_info_message(content, sid):
    socketio.emit("message", {"content": content, "style": "info"}, to=sid)

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
        if cur_ID == 0:
            admin = True

    socketio.emit("handshakeAnswer", {"ok" : ok, "admin" : admin}, to=request.sid)

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
