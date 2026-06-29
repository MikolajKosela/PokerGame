from typing import Any

from flask_socketio import SocketIO

from game import Game
from services.serialization import build_start_data, send_data, send_logs


def refresh_data(socketio: SocketIO, game: Game) -> None:
    socketio.emit("startData", build_start_data(game))
    send_logs(socketio, game)

    for player in game.players:
        send_data(socketio, game, player.sid)


def send_error_message(socketio: SocketIO, message: str | None, sid: str) -> None:
    socketio.emit(
        "message",
        {"content": message, "style": "err"},
        to=sid,
    )


def send_info_message(socketio: SocketIO, message: str | None, sid: str) -> None:
    socketio.emit(
        "message",
        {"content": message, "style": "info"},
        to=sid,
    )


def send_message_to_everyone(socketio: SocketIO, message: str) -> None:
    socketio.emit(
        "message",
        {"content": message, "style": None},
    )