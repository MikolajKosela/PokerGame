from app import app
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

@app.route("/commonCards")
def commonCards():
    tem = game.tables[-1]
    return jsonify(tem.to_dict())


@app.route("/yourCards")
def yourCards():
    tem = game.tables[session.get("ID")]
    return jsonify(tem.to_dict())

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


@app.route("/", methods=["GET", "POST"])
def start():
    return render_template("start.html")


@app.route("/lobby", methods=["GET", "POST"])
def lobby():
    return render_template("lobby.html")


@app.route("/action", methods=["POST", "GET"])
def action():
    '''
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
    '''
    return render_template("action.html")


@app.route("/wait")
def wait():
    '''
    if game.whoseRoundIs == -1:
        return redirect(url_for("lobby"))
    player_id = session.get("ID")
    '''
    return render_template("wait.html")

@app.route("/end", methods=["GET", "POST"])
def end():
    '''
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
    '''

    return render_template("end.html")
