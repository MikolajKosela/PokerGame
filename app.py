from card import Card
from pack import Pack
from table import Table
from player import Player
from game import Game
from flask import Flask, request, render_template, url_for, redirect, session, jsonify, session
import random
app = Flask(__name__)
app.secret_key="tajny klucz"

game=Game()

def checkState(methodNum):
    nickname=session.get("nickname")
    curID=session.get("ID")
    playerExist = False

    #0 - start
    #1 - lobby
    #2 - action
    #3 - wait
    #4 - end

    for player in game.players:
        if nickname == player.nickname:
            playerExist = True

    if playerExist == False and curID != None:
        session.clear()
        curID = None
        nickname = None
    
    if curID == None:
        if methodNum == 0:
            return None
        else:
            return redirect(url_for("start"))

    if game.isEnd == True:
        if methodNum == 4:
            return None
        else:
            return redirect(url_for("end"))

    if game.whoseRoundIs == -1:
        if methodNum == 1:
            return None
        else:
            return redirect(url_for("lobby"))

    if curID != game.whoseRoundIs:
        if methodNum == 3:
            return None
        else:
            return redirect(url_for("wait"))

    if curID == game.whoseRoundIs:
        if methodNum == 2:
            return None
        else:
            return redirect(url_for("action"))
    return None

@app.route("/players")
def get_players():
    players_list=[]
    for player in game.players:
        players_list.append(player.to_dict())
    return jsonify(players_list)

@app.route("/commonCards")
def commonCards():
    tem=game.tables[-1]
    return jsonify(tem.to_dict())

@app.route("/yourCards")
def yourCards():
    tem=game.tables[session.get("ID")]
    return jsonify(tem.to_dict())

@app.route("/wait")
def wait():
    if game.whoseRoundIs==-1:
        return redirect(url_for("lobby"))
    player_id=session.get("ID")
    return render_template("wait.html")

@app.route("/whoseRound")
def whoseRound():
    if game.whoseRoundIs>=0:
        roundData={
                "yourId": session.get("ID"),
                "round": game.whoseRoundIs,
                "playerName": game.players[game.whoseRoundIs].nickname,
                "playerCredit": game.players[game.whoseRoundIs].credits,
                "pot": game.pot,
                "bet": game.bet-game.players[session.get("ID")].bet,
                "checkButton": game.players[session.get("ID")].allin or game.bet==game.players[session.get("ID")].bet,
                "betButton": not game.players[session.get("ID")].allin and game.roundNum%2==0 and game.bet==0,
                "callButton": not game.players[session.get("ID")].allin and game.bet>game.players[session.get("ID")].bet,
                "raiseButton": not game.players[session.get("ID")].allin and game.roundNum%2==0 and game.bet>0,
                "foldButton": not game.players[session.get("ID")].allin and True,
                "allinButton": game.roundNum%2==0 and game.players[session.get("ID")].credits>0,
                "playerBet": game.players[session.get("ID")].bet,
                "roundNum": game.roundNum,
                "allin": game.players[session.get("ID")].allin
        }
        return jsonify(roundData)
    else:
        roundData={
                "yourId": session.get("ID"),
                "round": game.whoseRoundIs,
                "pot": game.pot,
        }
        return jsonify(roundData)

@app.route("/", methods=["GET", "POST"])
def start():
    state = checkState(0)
    if state is not None:
        return state

    if request.method=="POST":
        nickname=request.form["nickname"]
        session["nickname"]=nickname
        session["ID"]=len(game.players)
        game.players.append(Player(nickname, 99, len(game.players)))
        game.playersNum=len(game.players)
        return redirect(url_for("lobby"))
    return  render_template("start.html")


@app.route("/lobby", methods=["GET", "POST"])
def lobby():
    state = checkState(1)
    if state is not None:
        return state

    nickname=session.get("nickname")

    if request.method=="POST":
        return game.start()
    return render_template("lobby.html", nickname=nickname)

@app.route("/action", methods=["POST", "GET"])
def action():
    state = checkState(2)
    if state is not None:
        return state

    if request.method=="POST":
        action = request.form.get("action")
        if action=="continue":
            return game.nextPlayer()
        elif action=="check":
            return game.check()
        elif action=="bet":
            amount = int(request.form.get("betValue", 0))
            return game.makeBet(amount)
        elif action=="call":
            return game.call()
        elif action=="raise":
            amount = int(request.form.get("raiseValue", 0))
            return game.raiseBet(amount)
        elif action=="fold":
            return game.fold()
        elif action=="allin":
            return game.allin()
        return redirect(url_for("wait"))
    return render_template("action.html", roundNum=game.roundNum)

@app.route("/end", methods=["GET", "POST"])
def end():
    state = checkState(4)
    if state is not None:
        return state

    if request.method=="POST":
        action=request.form.get("action")
        if action=="again":
            if game.pot==0:
                return game.again()
            else:
                return render_template("end.html");
        winnerId=int(action)
        if(action!="again" and winnerId>=0 and winnerId<len(game.players)):
            game.players[winnerId].credits+=game.pot
            game.pot=0
    if game.isEnd==True:
        return render_template("end.html")
    return redirect(url_for("start"))

if __name__ == '__main__':
    app.run(debug = True)
