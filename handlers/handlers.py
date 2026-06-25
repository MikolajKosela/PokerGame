from flask import request

from services.auth import grant_token, handshake
from services.serialization import send_data, build_start_data
from utils.utils import refresh_data, send_error_message
from services.validation import can_receive_action, can_start_game, can_choose_winners, can_join_game

def register_handlers(socketio, game):
    @socketio.on("handshake")
    def handshake_handler(data):
        result_data = handshake(socketio, game, data["token"], request.sid)
        socketio.emit("handshakeAnswer", result_data, to=request.sid)

    @socketio.on("startDataRequest")
    def start_data_request():
        socketio.emit("startData", build_start_data(game))

    @socketio.on("join")
    def join(data):
        nickname = data["nickname"]
        result = can_join_game(game, request.sid, nickname)

        if result.ok:
            game.append_player(nickname, 100, request.sid)
            socketio.emit("joined", {"token": grant_token(game)}, to=request.sid)
            refresh_data(socketio, game)
        else:
            send_error_message(socketio,result.info, request.sid)

    @socketio.on("startGame")
    def start_game():
        result = can_start_game(game, request.sid)

        if not result.ok:
            send_error_message(socketio,result.info, request.sid)
            return

        game.start()
        refresh_data(socketio, game)

    @socketio.on("gameDataRequest")
    def game_data_request():
        send_data(socketio, game, request.sid)

    @socketio.on("check")
    def check():
        print("check")
        result = can_receive_action(game, request.sid)

        if not result.ok:
            send_error_message(socketio,result.info, request.sid)
            return
        
        result = game.check(request.sid)

        if result is None:
            refresh_data(socketio, game)
        else:
            send_error_message(socketio,result.info, request.sid)

    @socketio.on("bet")
    def bet(data):
        amount = int(data["amount"])
        print("bet: ", amount)
        result = can_receive_action(game, request.sid)

        if not result.ok:
            send_error_message(socketio,result.info, request.sid)
            return

        result = game.make_bet(request.sid, amount)

        if result is None:
            refresh_data(socketio, game)
        else:
            send_error_message(socketio,result.info, request.sid)

    @socketio.on("call")
    def call():
        print("call")
        result = can_receive_action(game, request.sid)

        if not result.ok:
            send_error_message(socketio,result.info, request.sid)
            return
        
        result = game.call(request.sid)

        if result is None:
            refresh_data(socketio, game)
        else:
            send_error_message(socketio,result.info, request.sid)

    @socketio.on("raise")
    def raise_bet(data):
        amount = int(data["amount"])
        print("raise: ", amount)
        result = can_receive_action(game, request.sid)

        if not result.ok:
            send_error_message(socketio,result.info, request.sid)
            return

        result = game.raiseBet(request.sid, amount)

        if result is None:
            refresh_data(socketio, game)
        else:
            send_error_message(socketio,result.info, request.sid)

    @socketio.on("fold")
    def fold():
        print("fold")
        result = can_receive_action(game, request.sid)

        if not result.ok:
            send_error_message(socketio,result.info, request.sid)
            return

        result = game.fold(request.sid)

        if result is None:
            refresh_data(socketio, game)
        else:
            send_error_message(socketio,result.info, request.sid)

    @socketio.on("allin")
    def allin():
        print("allin")
        result = can_receive_action(game, request.sid)

        if not result.ok:
            send_error_message(socketio,result.info, request.sid)
            return

        result = game.allin(request.sid)

        if result is None:
            refresh_data(socketio, game)
        else:
            send_error_message(socketio,result.info, request.sid)

    @socketio.on("winners")
    def winners(data):
        result = can_choose_winners(game, request.sid)

        if not result.ok:
            send_error_message(socketio,result.info, request.sid)
            return

        winnersNum = len(data)
        if winnersNum != 0:
            for playerID in data:
                id = int(playerID)
                game.players[id].credits += game.pot // winnersNum
        
            game.pot %= winnersNum
        socketio.emit("creditsGranted")
        refresh_data(socketio, game)

    @socketio.on("newDeal")
    def newDeal():
        game.again()
        refresh_data(socketio, game)