from typing import Any

from flask_socketio import SocketIO

from game import Game


JsonDict = dict[str, Any]


def build_start_data(game: Game) -> JsonDict:
    return {
        "playersNum": game.players_num(),
        "started": game.started(),
    }


def build_summary_data(game: Game) -> JsonDict | None:
    if not game.is_end():
        return None

    history = [
        {"message": log.display_time + " - " + log.message}
        for log in game.history
    ]

    players = []

    for index, player in enumerate(game.players):
        cards = [card.to_dict() for card in game.tables[index].cards]

        players.append(
            {
                "nickname": player.nickname,
                "id": player.id,
                "fold": player.fold,
                "allIn": player.all_in,
                "credits": player.credits,
                "cards": cards,
                "result": player.result,
                "admin": player.id == game.admin_id,
            }
        )

    return {
        "players": players,
        "history": history,
        "gamePot": game.pot,
    }


def send_summary(socketio: SocketIO, game: Game) -> None:
    summary_data = build_summary_data(game)

    if summary_data is None:
        return

    socketio.emit("summary", summary_data)


def check_state(game: Game, sid: str) -> str:
    player = game.get_player_by_sid(sid)

    if player is None:
        return "/"

    if game.is_end():
        return "/end"

    if game.whose_round_is == -1:
        return "/lobby"

    return "/game"


def build_buttons(game: Game, sid: str) -> JsonDict:
    player = game.get_player_by_sid(sid)

    if player is None:
        return {
            "check": False,
            "bet": False,
            "call": False,
            "raise": False,
            "fold": False,
            "allIn": False,
        }

    return {
        "check": player.can_check(game),
        "bet": player.can_bet(game),
        "call": player.can_call(game),
        "raise": player.can_raise(game),
        "fold": player.can_fold(game),
        "allIn": player.can_all_in(game),
    }


def build_game_logs(game: Game) -> list[JsonDict]:
    return [
        {"message": log.display_time + " - " + log.message}
        for log in game.event_queue
    ]


def send_logs(socketio: SocketIO, game: Game) -> None:
    if len(game.event_queue) == 0:
        return

    logs = build_game_logs(game)
    game.event_queue = []
    socketio.emit("logs", logs)


def build_round_data(game: Game, sid: str) -> JsonDict | None:
    player = game.get_player_by_sid(sid)

    if player is None:
        return None

    cur_nick = None

    if game.whose_round_is >= 0:
        cur_nick = game.players[game.whose_round_is].nickname

    return {
        "yourRound": player.id == game.whose_round_is,
        "curNick": cur_nick,
        "playersNum": game.players_num(),
        "pot": game.pot,
        "bet": game.bet - player.bet,
        "roundNum": int(game.round),
        "credits": player.credits,
        "lastRoundSkipped": game.last_round_skipped,
        "yourRoundSkipped": player.last_round_skipped,
    }


def build_common_cards(game: Game) -> JsonDict | None:
    if len(game.tables) == 0:
        return None

    return game.tables[-1].to_dict()


def build_player_cards(game: Game, sid: str) -> JsonDict | None:
    player = game.get_player_by_sid(sid)

    if player is None:
        return None

    return game.tables[player.id].to_dict()


def build_players_list(game: Game) -> list[JsonDict]:
    players = []

    for player in game.players:
        player_data = player.to_dict()
        player_data["admin"] = player.id == game.admin_id
        players.append(player_data)

    return players


def send_data(socketio: SocketIO, game: Game, sid: str) -> None:
    state = check_state(game, sid)
    player = game.get_player_by_sid(sid)

    common_cards = None
    player_cards = None
    round_data = None
    buttons = None

    if player is not None:
        if game.whose_round_is == player.id:
            buttons = build_buttons(game, sid)

        if game.started():
            common_cards = build_common_cards(game)
            player_cards = build_player_cards(game, sid)
            round_data = build_round_data(game, sid)

    data = {
        "state": state,
        "commonCards": common_cards,
        "playerCards": player_cards,
        "roundData": round_data,
        "buttons": buttons,
        "players": build_players_list(game),
    }

    if game.is_end():
        send_summary(socketio, game)

    socketio.emit("gameData", data, to=sid)