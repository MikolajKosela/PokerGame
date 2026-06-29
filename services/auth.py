from secrets import token_urlsafe
from typing import TypedDict

from game import Game


class HandshakeData(TypedDict):
    ok: bool
    admin: bool


def handshake(game: Game, token: object, sid: str) -> HandshakeData:
    player_id = check_token(game, token)

    if player_id is None:
        return {"ok": False, "admin": False}

    if not 0 <= player_id < len(game.players):
        return {"ok": False, "admin": False}

    game.sid_to_player[sid] = player_id
    game.players[player_id].sid = sid

    return {
        "ok": True,
        "admin": player_id == game.admin_id,
    }


def grant_token(game: Game, player_id: int) -> str:
    token = token_urlsafe(32)

    while token in game.token_to_player:
        token = token_urlsafe(32)

    game.token_to_player[token] = player_id
    return token


def check_token(game: Game, token: object) -> int | None:
    return game.token_to_player.get(str(token))