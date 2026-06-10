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

app = Flask(__name__)
socketio = SocketIO(app)
app.secret_key = "tajny klucz"

game = Game()

def grantID():
    id = random.randint(1000, 100000)
    while id in game.idToPlayer.keys():
        id = random.randint(1000, 100000)

    game.idToPlayer[id] = len(game.idToPlayer)
    return id

def checkID(id):
    id = int(id)

    print(game.idToPlayer)
    if id in game.idToPlayer.keys():
        return True
    return False 

@socketio.on("handshake")
def handshake(data):
    ok = False
    if checkID(data["gameID"] == True):
        ok = True

    socketio.emit("handshakeAnswer", {"ok" : ok}, to=request.sid)

@socketio.on("checkStateRequest")
def checkState():
    nickname = session.get("nickname")
    curID = session.get("ID")
    playerExist = False

    state = 0
    # 0 - start
    # 1 - lobby
    # 2 - action
    # 3 - wait
    # 4 - end

    '''
    if playerExist == False and curID != None:
        session.clear()
        curID = None
        nickname = None
    '''

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


@app.route("/players")
def get_players():
    players_list = []
    for player in game.players:
        players_list.append(player.to_dict())
    return jsonify(players_list)


@app.route("/commonCards")
def commonCards():
    tem = game.tables[-1]
    return jsonify(tem.to_dict())


@app.route("/yourCards")
def yourCards():
    tem = game.tables[session.get("ID")]
    return jsonify(tem.to_dict())


@app.route("/wait")
def wait():
    if game.whoseRoundIs == -1:
        return redirect(url_for("lobby"))
    player_id = session.get("ID")
    return render_template("wait.html")


@app.route("/whoseRound")
def whoseRound():
    if game.whoseRoundIs >= 0:
        roundData = {
            "yourId": session.get("ID"),
            "round": game.whoseRoundIs,
            "playerName": game.players[game.whoseRoundIs].nickname,
            "playerCredit": game.players[game.whoseRoundIs].credits,
            "pot": game.pot,
            "bet": game.bet - game.players[session.get("ID")].bet,
            "checkButton": game.players[session.get("ID")].allin
            or game.bet == game.players[session.get("ID")].bet,
            "betButton": not game.players[session.get("ID")].allin
            and game.roundNum % 2 == 0
            and game.bet == 0,
            "callButton": not game.players[session.get("ID")].allin
            and game.bet > game.players[session.get("ID")].bet,
            "raiseButton": not game.players[session.get("ID")].allin
            and game.roundNum % 2 == 0
            and game.bet > 0,
            "foldButton": not game.players[session.get("ID")].allin and True,
            "allinButton": game.roundNum % 2 == 0
            and game.players[session.get("ID")].credits > 0,
            "playerBet": game.players[session.get("ID")].bet,
            "roundNum": game.roundNum,
            "allin": game.players[session.get("ID")].allin,
        }
        return jsonify(roundData)
    else:
        roundData = {
            "yourId": session.get("ID"),
            "round": game.whoseRoundIs,
            "pot": game.pot,
        }
        return jsonify(roundData)


@app.route("/summary")
def sumarry():
    if game.isEnd == True:
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
        return jsonify(summaryData)
    else:
        return jsonify({"error": "Unauthorized"}), 403


@socketio.on("join")
def join(data):
    state = checkState()
    if state is not None:
        return state

    nickname = data["nickname"]
    session["nickname"] = nickname
    session["ID"] = len(game.players)
    game.players.append(Player(nickname, 99, len(game.players)))
    game.playersNum = len(game.players)

    socketio.emit("joined", {"gameID": grantID()}, to=request.sid)


@app.route("/", methods=["GET", "POST"])
def start():
    return render_template("start.html")


@app.route("/lobby", methods=["GET", "POST"])
def lobby():
    '''
    print("jestem w lobby")
    nickname = session.get("nickname")

    if request.method == "POST":
        game.start()
        if session.get("ID") == game.whoseRoundIs:
            return redirect(url_for("action"))
        else:
            return redirect(url_for("wait"))
    '''
    return render_template("lobby.html")


@app.route("/action", methods=["POST", "GET"])
def action():
    if request.method == "POST":
        action = request.form.get("action")
        if action == "continue":
            game.nextPlayer()
        elif action == "check":
            game.check()
        elif action == "bet":
            amount = int(request.form.get("betValue", 0))
            game.makeBet(amount)
        elif action == "call":
            game.call()
        elif action == "raise":
            amount = int(request.form.get("raiseValue", 0))
            game.raiseBet(amount)
        elif action == "fold":
            game.fold()
        elif action == "allin":
            game.allin()
        return redirect(url_for("wait"))
    return render_template("action.html", roundNum=game.roundNum)


@app.route("/end", methods=["GET", "POST"])
def end():
    state = checkState(4)
    if state is not None:
        return state

    if request.method == "POST":
        action = request.form.get("action")
        if action == "again":
            if game.pot == 0:
                return game.again()
            else:
                return render_template("end.html")
        winnerId = int(action)
        if action != "again" and winnerId >= 0 and winnerId < len(game.players):
            game.players[winnerId].credits += game.pot
            game.pot = 0
    if game.isEnd == True:
        return render_template("end.html")
    return redirect(url_for("start"))


if __name__ == "__main__":
    app.run(debug=True)
