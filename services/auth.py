from secrets import token_urlsafe

def handshake(socketio, game, token, sid):
    playerID = check_token(game, token) 

    if playerID is None:
        return {"ok" : False}

    game.sid_to_player[sid] = playerID 

    if playerID >= 0 and playerID < len(game.players):
        game.players[playerID].sid = sid

        return {"ok" : True, "admin" : playerID == game.adminID}

    return {"ok" : False}

def grant_token(game):
    token = token_urlsafe(32)
    while token in game.sid_to_player.keys():
        token = token_urlsafe(32)

    game.token_to_player[str(token)] = len(game.sid_to_player)
    return token

def check_token(game, token):
    token = str(token)

    if token in game.token_to_player.keys():
        return game.token_to_player[token]
    return None 