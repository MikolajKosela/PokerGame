from card import Card
from pack import Pack
from table import Table
from player import Player
from game import Game
from flask import (
    Flask,
    request,
    render_template,
    url_for,
    redirect,
    jsonify,
    session,
)
from flask_socketio import SocketIO, emit
import random
from app import *

socketio = SocketIO(app)

def grantToken():
    print("            przyznaje token")
    id = random.randint(1000, 100000)
    while id in game.idToPlayer.keys():
        id = random.randint(1000, 100000)

    game.idToPlayer[id] = len(game.idToPlayer)
    return id

def checkToken(token):
    token = str(token)
    if token.isdecimal() == False:
        return False

    token = int(token)

    print(game.idToPlayer)
    if token in game.idToPlayer.keys():
        return True
    return False 

def summary():
    if game.isEnd == False:
        return False
    summaryData = []
    for i, player in enumerate(game.players):
        cards = [card.to_dict() for card in game.tables[i].cards]
        summaryData.append(
            {
                "nickname": player.nickname,
                "id": player.ID,
                "fold": player.fold,
                "credits": player.credits,
                "cards": cards,
            }
        )

    socketio.emit("summary", summaryData)

@socketio.on("handshake")
def handshake(data):
    ok = False
    print(data)
    if checkToken(data["token"]) == True:
        ok = True

    admin = False

    if ok == True:
        curID = game.idToPlayer[int(data["token"])]
        session["ID"] = curID
        session["nickname"] = game.players[curID].nickname
        print(session)
        if curID == 0:
            admin = True

    socketio.emit("handshakeAnswer", {"ok" : ok, "admin" : admin}, to=request.sid)

@socketio.on("checkStateRequest")
def checkState():
    nickname = session.get("nickname")
    curID = session.get("ID")

    state = "/"
    # 0 - start
    # 1 - lobby
    # 2 - action
    # 3 - wait
    # 4 - end
    print (curID, game.isEnd, game.whoseRoundIs)

    if curID == None:
        state = "/"
    elif game.isEnd == True:
        state = "/end"
    elif game.whoseRoundIs == -1:
        state = "/lobby"
    elif curID == game.whoseRoundIs:
        state = "/action"
    elif curID != game.whoseRoundIs:
        state = "/wait"

    print("Dostałem zapytanie, wysyłam", state)
    socketio.emit("checkState", {"state": state}, to=request.sid)

@socketio.on("join")
def join(data):
    nickname = data["nickname"]
    session["nickname"] = nickname
    session["ID"] = len(game.players)
    game.players.append(Player(nickname, 99, len(game.players)))
    game.playersNum = len(game.players)

    print("Dołączył gracz")
    socketio.emit("joined", {"token": grantToken()}, to=request.sid)

@socketio.on("playersListRequest")
def playersList():
    playersList = [player.to_dict() for player in game.players]

    socketio.emit("playersList", playersList)

@socketio.on("startGame")
def startGame():
    if session.get("ID") == 0:
        game.start()
        socketio.emit("started")
    

@socketio.on("gameDataRequest")
def gameDataRequest():
    myID = None
    myData = None
    curID = None
    curNick = None
    playersNum = None
    pot = None 
    bet = None 
    roundNum = None
    yourBet = None
    yourCredits = None 

    commonCards = None 
    playerCards = None
    roundData = None 
    players = None 
    buttons = None 

    myID = session.get("ID")
    playersNum = len(game.players)

    if (game.whoseRoundIs >= 0 or game.isEnd) and myID != None:
        myData = game.players[myID]
        commonCards = game.tables[-1].to_dict()
        playerCards = game.tables[myID].to_dict()
        curID = game.whoseRoundIs
        curNick = game.players[curID].nickname
        pot = game.pot
        bet = game.bet - myData.bet
        roundNum = game.roundNum
        yourBet = myData.bet
        yourCredits = myData.credits
        buttons = {
            "check": myData.allin or game.bet == myData.bet,
            "bet": not myData.allin and game.roundNum % 2 == 0 and game.bet == 0,
            "call": not myData.allin and game.bet > myData.bet,
            "raise": not myData.allin and game.roundNum % 2 == 0 and game.bet > 0,
            "fold": not myData.allin, 
            "allin": myData.credits > 0 and game.roundNum % 2 == 0
        }
        players = [player.to_dict() for player in game.players]

    roundData = {
        "curID": curID,
        "curNick": curNick,
        "playersNum": playersNum,
        "pot": pot, 
        "bet": bet,
        "roundNum": roundNum,
        "yourBet": yourBet,
        "yourCredits": yourCredits,
    }
    
    data = {
        "commonCards": commonCards,
        "playerCards": playerCards,
        "roundData": roundData,
        "buttons": buttons,
        "players": players
    }

    if game.isEnd == True:
        summary()
    socketio.emit("gameData", data, to=request.sid)

@socketio.on("check")
def check():
    print("check")

    myData = game.players[session.get("ID")]
    if not(myData.allin or game.bet == myData.bet):
        socketio.emit("checkState", {"state": "/action"}, to=request.sid)
        return False
    
    game.check()
    socketio.emit("actionMade")
    return True

@socketio.on("bet")
def bet(data):
    amount = data["amount"]
    amount = str(amount)
    amount = int(amount)
    print("bet: ", amount)

    myData = game.players[session.get("ID")]

    if not(not myData.allin and game.roundNum % 2 == 0 and game.bet == 0):
        socketio.emit("checkState", {"state": "/action"}, to=request.sid)
        return False


    game.makeBet(amount)
    socketio.emit("actionMade")
    return True

@socketio.on("call")
def call():
    print("call")

    myData = game.players[session.get("ID")]
    if not(not myData.allin and game.bet > myData.bet):
        socketio.emit("checkState", {"state": "/action"}, to=request.sid)
        return False
    
    game.call()
    socketio.emit("actionMade")
    return True

@socketio.on("raise")
def raiseBet(data):
    amount = data["amount"]
    amount = str(amount)
    amount = int(amount)
    print("raise: ", amount)

    myData = game.players[session.get("ID")]

    if not(not myData.allin and game.roundNum % 2 == 0 and game.bet > 0):
        socketio.emit("checkState", {"state": "/action"}, to=request.sid)
        return False

    game.raiseBet(amount)
    socketio.emit("actionMade")
    return True

@socketio.on("fold")
def fold():
    print("fold")

    myData = game.players[session.get("ID")]

    if not(not myData.allin):
        socketio.emit("checkState", {"state": "/action"}, to=request.sid)
        return False
    
    game.fold()
    socketio.emit("actionMade")
    return True

@socketio.on("allin")
def allin():
    print("allin")

    myData = game.players[session.get("ID")]

    if not(myData.credits > 0 and game.roundNum % 2 == 0):
        socketio.emit("checkState", {"state": "/action"}, to=request.sid)
        return False
    
    game.allin()
    socketio.emit("actionMade")
    return True

@socketio.on("winners")
def winners(data):
    winnersNum = len(data)
    for player in data:
        id = int(player)
        game.players[id].credits += game.pot // winnersNum
    
    game.pot %= winnersNum
    socketio.emit("creditsGranted")

@socketio.on("newDeal")
def newDeal():
    game.again()
    socketio.emit("checkState", {"state": "/wait"})
