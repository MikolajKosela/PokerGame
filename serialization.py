from card import Card
from pack import Pack
from table import Table
from player import Player
from game import Game

from flask_socketio import emit
from app import app, game, socketio 

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