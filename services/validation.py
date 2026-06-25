from models import Result

def can_receive_action(game, sid):
    player = game.get_player_by_sid(sid)

    if not game.started():
        return Result(False, "Invalid query", "Nie możesz wykonać tej akcji. Gra się jeszcze nie zaczęła")

    if game.is_end():
        return Result(False, "Invalid query", "Nie możesz wykonać tej akcji. Gra się już skończyła")

    if player is None:
        return Result(False, "Permission denied", "Nie możesz wykonać tej akcji. Nie jesteś graczem")

    if player.ID != game.current_player().ID:
        return Result(False, "Permission denied", "Nie możesz wykonać tej akcji. Nie Twoja kolej")

    return Result(True)

def can_start_game(game, sid):
    player = game.get_player_by_sid(sid)

    if player is None:
        return Result(False, "Permission denied", "Nie możesz rozpocząć gry. Nie jesteś graczem")

    if game.started():
        return Result(False, "Invalid query", "Rozgrywka już się rozpoczęła")

    if player.ID != game.adminID:
        return Result(False, "Permission denied", "Tylko admin może rozpocząć rozgrywkę")

    return Result(True)

def can_choose_winners(game, sid):
    player = game.get_player_by_sid(sid)

    if player is None:
        return Result(False, "Permission denied", "Nie możesz rozpocząć gry. Nie jesteś graczem")

    if player.ID != game.adminID:
        return Result(False, "Permission denied", "Tylko admin może wybrać zwycięzców")

    if not game.is_end():
        return Result(False, "Invalid query", "Tylko admin może wybrać zwycięzców")

    return Result(True)

def can_join_game(game, sid, nickname):
    if game.started():
        return Result(False, "Invalid query", "Nie możesz dołączyć w trakcie trwającej rozgrywki")

    if game.get_player_by_sid(sid) != None:
        return Result(False, "Invalid query", "Nie możesz dołączyć ponownie, bo już jesteś graczem")

    if len(nickname) == 0 :
            return Result(False, "Invalid data", "Nick nie moży być pusty")

    if not all(char.isalnum() or char == "_" for char in nickname):
        return Result(False,  "Invalid data", "Nick może składać się z tylko z znaków a-z, 0-9, _")

    if any(player.nickname == nickname for player in game.players):
        return Result(False, "Invalid query", "Gracz o takim nicku istnieje")

    return Result(True)
