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

@app.route("/", methods=["GET", "POST"])
def start():
    return render_template("start.html")


@app.route("/lobby", methods=["GET", "POST"])
def lobby():
    return render_template("lobby.html")

@app.route("/action", methods=["POST", "GET"])
def action():
    return render_template("action.html")


@app.route("/wait")
def wait():
    return render_template("wait.html")

@app.route("/end", methods=["GET", "POST"])
def end():
    return render_template("end.html")
