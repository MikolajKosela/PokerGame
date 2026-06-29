from game import Game
from models import Result


def can_receive_action(game: Game, sid: str) -> Result:
    player = game.get_player_by_sid(sid)
    current_player = game.current_player()

    if not game.started():
        return Result(
            False,
            "Invalid query",
            "Nie możesz wykonać tej akcji. Gra się jeszcze nie zaczęła",
        )

    if game.is_end():
        return Result(
            False,
            "Invalid query",
            "Nie możesz wykonać tej akcji. Gra się już skończyła",
        )

    if player is None:
        return Result(
            False,
            "Permission denied",
            "Nie możesz wykonać tej akcji.\nNie jesteś graczem",
        )

    if current_player is None:
        return Result(
            False,
            "Invalid state",
            "Nie ma obecnie aktywnego gracza",
        )

    if player.id != current_player.id:
        return Result(
            False,
            "Permission denied",
            "Nie możesz wykonać tej akcji. Nie Twoja kolej",
        )

    return Result(True)


def can_start_game(game: Game, sid: str) -> Result:
    player = game.get_player_by_sid(sid)

    if player is None:
        return Result(
            False,
            "Permission denied",
            "Nie możesz rozpocząć gry.\nNie jesteś graczem",
        )

    if game.started():
        return Result(False, "Invalid query", "Rozgrywka już się rozpoczęła")

    if player.id != game.admin_id:
        return Result(
            False,
            "Permission denied",
            "Tylko admin może rozpocząć rozgrywkę",
        )

    return Result(True)


def can_choose_winners(game: Game, sid: str) -> Result:
    player = game.get_player_by_sid(sid)

    if player is None:
        return Result(
            False,
            "Permission denied",
            "Nie możesz wybrać zwycięzców.\nNie jesteś graczem",
        )

    if player.id != game.admin_id:
        return Result(
            False,
            "Permission denied",
            "Tylko admin może wybrać zwycięzców",
        )

    if not game.is_end():
        return Result(
            False,
            "Invalid query",
            "Zwycięzców można wybrać dopiero po zakończeniu rozdania",
        )

    return Result(True)


def can_join_game(game: Game, sid: str, nickname: str) -> Result:
    if game.started():
        return Result(
            False,
            "Invalid query",
            "Nie możesz dołączyć w trakcie trwającej rozgrywki",
        )

    if game.get_player_by_sid(sid) is not None:
        return Result(
            False,
            "Invalid query",
            "Nie możesz dołączyć ponownie, bo już jesteś graczem",
        )

    if len(nickname) == 0:
        return Result(False, "Invalid data", "Nick nie może być pusty")

    if not all(char.isalnum() or char == "_" for char in nickname):
        return Result(
            False,
            "Invalid data",
            "Nick może składać się tylko ze znaków a-z, 0-9, _",
        )

    if any(player.nickname == nickname for player in game.players):
        return Result(False, "Invalid query", "Gracz o takim nicku istnieje")

    return Result(True)