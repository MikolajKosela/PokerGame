def build_start_data(game):
    data = {
        "playersNum": game.players_num(),
        "started": game.started()
    }
    return data

def summary(socketio, game):
    if not game.is_end():
        return False
    sumarry_data = []

    history = []
    for log in game.history:
        history.append({"message": log.display_time + " - " + log.message})

    players = []
    for i, player in enumerate(game.players):
        cards = [card.to_dict() for card in game.tables[i].cards]
        
        players.append(
            {
                "nickname": player.nickname,
                "id": player.ID,
                "fold": player.fold,
                "allin": player.allin,
                "credits": player.credits,
                "cards": cards,
                "result": player.result,
                "admin": player.ID == game.adminID,
            }
        )
    
    sumarry_data = {
        "players": players,
        "history": history,
        "gamePot": game.pot,
    }
    socketio.emit("summary", sumarry_data)

def check_state(game, sid):
    cur_ID = game.get_player_by_sid(sid)

    state = "/"
    # 0 - start
    # 1 - lobby
    # 2 - action
    # 3 - wait
    # 4 - end
    print (cur_ID, game.is_end(), game.whose_round_is)

    if cur_ID is None:
        state = "/"
    elif game.is_end():
        state = "/end"
    elif game.whose_round_is == -1:
        state = "/lobby"
    else:
        state="/game"

    print("Dostałem zapytanie od", cur_ID, "wysyłam", state)
    return state

def build_buttons(game, sid):
    player = game.get_player_by_sid(sid)

    buttons = {
        "check": player.can_check(game),
        "bet": player.can_bet(game),
        "call": player.can_call(game),
        "raise": player.can_raise(game),
        "fold": player.can_fold(game),
        "allin": player.can_allin(game),
    } 

    return buttons 

def build_game_logs(game):
    logs = []

    for log in game.event_queue:
        logs.append({"message": log.display_time + " - " + log.message})
    return logs

def send_logs(socketio, game):
    if len(game.event_queue) > 0:
        logs = build_game_logs(game)
        game.event_queue = []
        socketio.emit("logs", logs)

def build_round_data(game, sid):
    player = game.get_player_by_sid(sid)

    cur_nick = None
    if game.whose_round_is >= 0:
        cur_nick = game.players[game.whose_round_is].nickname,

    round_data = {
        "yourRound": player.ID == game.whose_round_is,
        "curNick": cur_nick,
        "playersNum": game.players_num(),
        "pot": game.pot, 
        "bet": game.bet - player.bet,
        "roundNum": game.round,
        "credits": player.credits,
        "lastRoundSkipped": game.last_round_skipped,
        "yourRoundSkipped": player.last_round_skipped
    }
    
    return round_data
    
def build_common_cards(game):
    return game.tables[-1].to_dict()

def build_player_cards(game, sid):
    player = game.get_player_by_sid(sid)
    return game.tables[player.ID].to_dict()

def build_players_list(game):
    player_list = []
    for player in game.players:
        p = player.to_dict()
        p["admin"] = p["id"] == game.adminID
        player_list.append(p)

    return player_list

def send_data(socketio, game, sid):
    print("Wysyłam dane do gracza: ", sid)
    state = "/" 
    common_cards = None 
    player_cards = None
    round_data = None 
    players = build_players_list(game) 
    buttons = None 

    if game.sid_to_player.get(sid) is not None:
        state = check_state(game, sid)

        player = game.get_player_by_sid(sid)
        if game.whose_round_is == player.ID:
            buttons = build_buttons(game, sid)

    if game.started():
        common_cards = build_common_cards(game)
        player_cards = build_player_cards(game, sid)
        round_data = build_round_data(game, sid)


    data = {
        #"sid": sid,
        "state": state,
        "commonCards": common_cards,
        "playerCards": player_cards,
        "roundData": round_data,
        "buttons": buttons,
        "players": players
    }

    if game.is_end():
        summary(socketio, game)
    socketio.emit("gameData", data, to=sid)