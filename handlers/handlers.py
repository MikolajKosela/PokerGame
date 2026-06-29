from typing import Any, Callable

from flask import request
from flask_socketio import SocketIO

from game import Game
from models import Result
from services.auth import grant_token, handshake
from services.serialization import build_start_data, send_data
from services.validation import (
    can_choose_winners,
    can_join_game,
    can_receive_action,
    can_start_game,
)
from utils.utils import refresh_data, send_error_message


JsonDict = dict[str, Any]
GameAction = Callable[[str], Result]


def handle_result(socketio: SocketIO, game: Game, result: Result, sid: str) -> None:
    if result.ok:
        refresh_data(socketio, game)
        return

    send_error_message(socketio, result.info, sid)


def register_handlers(socketio: SocketIO, game: Game) -> None:
    @socketio.on("handshake")
    def handshake_handler(data: JsonDict) -> None:
        token = data.get("token")
        result_data = handshake(game, token, request.sid)
        socketio.emit("handshakeAnswer", result_data, to=request.sid)

    @socketio.on("startDataRequest")
    def start_data_request() -> None:
        socketio.emit("startData", build_start_data(game), to=request.sid)

    @socketio.on("join")
    def join(data: JsonDict) -> None:
        nickname = str(data.get("nickname", "")).strip()
        result = can_join_game(game, request.sid, nickname)

        if not result.ok:
            send_error_message(socketio, result.info, request.sid)
            return

        game.append_player(nickname, 100, request.sid)
        player = game.get_player_by_sid(request.sid)

        if player is None:
            send_error_message(
                socketio,
                "Nie udało się utworzyć gracza",
                request.sid,
            )
            return

        socketio.emit(
            "joined",
            {"token": grant_token(game, player.id)},
            to=request.sid,
        )
        refresh_data(socketio, game)

    @socketio.on("startGame")
    def start_game() -> None:
        result = can_start_game(game, request.sid)

        if not result.ok:
            send_error_message(socketio, result.info, request.sid)
            return

        game.start()
        refresh_data(socketio, game)

    @socketio.on("gameDataRequest")
    def game_data_request() -> None:
        send_data(socketio, game, request.sid)

    def handle_game_action(action: GameAction) -> None:
        result = can_receive_action(game, request.sid)

        if not result.ok:
            send_error_message(socketio, result.info, request.sid)
            return

        result = action(request.sid)
        handle_result(socketio, game, result, request.sid)

    @socketio.on("check")
    def check() -> None:
        handle_game_action(game.check)

    @socketio.on("bet")
    def bet(data: JsonDict) -> None:
        try:
            amount = int(data["amount"])
        except (KeyError, TypeError, ValueError):
            send_error_message(socketio, "Nieprawidłowa wartość zakładu", request.sid)
            return

        handle_game_action(lambda sid: game.make_bet(sid, amount))

    @socketio.on("call")
    def call() -> None:
        handle_game_action(game.call)

    @socketio.on("raise")
    def raise_bet(data: JsonDict) -> None:
        try:
            amount = int(data["amount"])
        except (KeyError, TypeError, ValueError):
            send_error_message(socketio, "Nieprawidłowa wartość podbicia", request.sid)
            return

        handle_game_action(lambda sid: game.raise_bet(sid, amount))

    @socketio.on("fold")
    def fold() -> None:
        handle_game_action(game.fold)

    @socketio.on("allin")
    def all_in() -> None:
        handle_game_action(game.all_in)

    @socketio.on("winners")
    def winners(data: JsonDict) -> None:
        result = can_choose_winners(game, request.sid)

        if not result.ok:
            send_error_message(socketio, result.info, request.sid)
            return

        winner_ids = [int(player_id) for player_id in data]
        winners_num = len(winner_ids)

        if winners_num == 0:
            send_error_message(socketio, "Musisz wybrać co najmniej jednego zwycięzcę", request.sid)
            return

        prize = game.pot // winners_num
        remainder = game.pot % winners_num

        for player_id in winner_ids:
            game.players[player_id].credits += prize

        game.players[winner_ids[0]].credits += remainder
        game.pot = 0

        socketio.emit("creditsGranted")
        refresh_data(socketio, game)

    @socketio.on("newDeal")
    def new_deal() -> None:
        game.again()
        refresh_data(socketio, game)