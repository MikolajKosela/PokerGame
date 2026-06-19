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
)
from flask_socketio import SocketIO, emit
import random
from app import *

socketio = SocketIO(app)

def grantToken():
    token = random.randint(1000, 100000)
    while token in game.sidToPlayer.keys():
        token = random.randint(1000, 100000)

    game.tokenToPlayer[token] = len(game.sidToPlayer)
    return token

def checkToken(token):
    token = str(token)
    if token.isdecimal() == False:
        return False

    token = int(token)

    if token in game.tokenToPlayer.keys():
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

def checkState(sid):
    curID = game.sidToPlayer[sid]
    nickname = game.players[curID].nickname

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

    print("Dostałem zapytanie od", curID, nickname, "wysyłam", state)
    return state

def sendData(sid):
    print("Wysyłam dane do gracza: ", sid)
    state = "/"
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

    if game.sidToPlayer.get(sid) != None:
        myID = game.sidToPlayer[sid]
        state = checkState(sid)
        print(" ID GRACZA ", myID, game.players[myID].nickname)

    playersNum = len(game.players)
    players = [player.to_dict() for player in game.players]

    if (game.whoseRoundIs >= 0 or game.isEnd) and myID != None:
        myData = game.players[myID]
        commonCards = game.tables[-1].to_dict()
        playerCards = game.tables[myID].to_dict()
        curID = game.whoseRoundIs
        if curID >= 0:
            curNick = game.players[curID].nickname
        pot = game.pot
        bet = game.bet - myData.bet
        roundNum = game.roundNum
        yourBet = myData.bet
        yourCredits = myData.credits
        buttons = {
            "check": myData.allin or game.bet == myData.bet,
            "bet": not myData.allin and game.roundNum % 2 == 0 and game.bet == 0 and myData.credits > 0,
            "call": not myData.allin and game.bet > myData.bet and game.bet <= myData.credits,
            "raise": not myData.allin and game.roundNum % 2 == 0 and game.bet > 0 and myData.credits > game.bet,
            "fold": not myData.allin, 
            "allin": myData.credits > 0 and (game.roundNum % 2 == 0 or game.bet > myData.credits)
        }

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
        #"sid": sid,
        "state": state,
        "commonCards": commonCards,
        "playerCards": playerCards,
        "roundData": roundData,
        "buttons": buttons,
        "players": players
    }

    if game.isEnd == True:
        summary()
    socketio.emit("gameData", data, to=sid)

def refreshData():
    print("  Wyświetlam graczy, którym odświeżam dane")
    for player in game.players:
        print(player.nickname)
        sendData(player.sid)

@socketio.on("handshake")
def handshake(data):
    ok = False
    print(data)
    if checkToken(data["token"]) == True:
        ok = True

    admin = False

    if ok == True:
        curID = game.tokenToPlayer[int(data["token"])]
        game.sidToPlayer[request.sid] = curID
        if curID >= 0:
            game.players[curID].sid = request.sid
        if curID == 0:
            admin = True

    socketio.emit("handshakeAnswer", {"ok" : ok, "admin" : admin}, to=request.sid)

@socketio.on("lobbyUpdateRequest")
def lobbyUpdateRequest():
    socketio.emit("lobbyUpdate", {"playersNum": len(game.players)})

@socketio.on("join")
def join(data):
    nickname = data["nickname"]
    game.players.append(Player(nickname, 100, len(game.players), request.sid))
    game.playersNum = len(game.players)

    socketio.emit("joined", {"token": grantToken()}, to=request.sid)
    socketio.emit("lobbyUpdate", {"playersNum": len(game.players)})
    refreshData()

@socketio.on("startGame")
def startGame():
    if game.sidToPlayer[request.sid] == 0:
        game.start()
        refreshData()

@socketio.on("gameDataRequest")
def gameDataRequest():
    sendData(request.sid)

@socketio.on("check")
def check():
    print("check")

    myData = game.players[game.sidToPlayer[request.sid]]
    if not(myData.allin or game.bet == myData.bet):
        socketio.emit("error", {"info": "serwer odrzucił przekazane dane"}, to=request.sid)
        return False
    
    game.check(request.sid)
    refreshData()

@socketio.on("bet")
def bet(data):
    amount = data["amount"]
    amount = str(amount)
    amount = int(amount)
    print("bet: ", amount)

    myData = game.players[game.sidToPlayer[request.sid]]

    if not(not myData.allin and game.roundNum % 2 == 0 and game.bet == 0):
        socketio.emit("error", {"info": "serwer odrzucił przekazane dane"}, to=request.sid)
        return False

    game.makeBet(request.sid, amount)
    refreshData()

@socketio.on("call")
def call():
    print("call")

    myData = game.players[game.sidToPlayer[request.sid]]
    if not(not myData.allin and game.bet > myData.bet):
        socketio.emit("error", {"info": "serwer odrzucił przekazane dane"}, to=request.sid)
        return False
    
    game.call(request.sid)
    refreshData()

@socketio.on("raise")
def raiseBet(data):
    amount = data["amount"]
    amount = str(amount)
    amount = int(amount)
    print("raise: ", amount)

    myData = game.players[game.sidToPlayer[request.sid]]

    if not(not myData.allin and game.roundNum % 2 == 0 and game.bet > 0):
        socketio.emit("error", {"info": "serwer odrzucił przekazane dane"}, to=request.sid)
        return False

    game.raiseBet(request.sid, amount)
    refreshData()

@socketio.on("fold")
def fold():
    print("fold")

    myData = game.players[game.sidToPlayer[request.sid]]

    if not(not myData.allin):
        socketio.emit("error", {"info": "serwer odrzucił przekazane dane"}, to=request.sid)
        return False
    
    game.fold(request.sid)
    refreshData()

@socketio.on("allin")
def allin():
    print("allin")

    myData = game.players[game.sidToPlayer[request.sid]]

    if not(myData.credits > 0 and game.roundNum % 2 == 0):
        socketio.emit("error", {"info": "serwer odrzucił przekazane dane"}, to=request.sid)
        return False
    
    game.allin(request.sid)
    refreshData()

@socketio.on("winners")
def winners(data):
    winnersNum = len(data)
    for player in data:
        id = int(player)
        game.players[id].credits += game.pot // winnersNum
    
    game.pot %= winnersNum
    socketio.emit("creditsGranted")
    refreshData()

@socketio.on("newDeal")
def newDeal():
    game.again()
    refreshData()
