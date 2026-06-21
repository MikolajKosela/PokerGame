from app import app
from flask import render_template

@app.route("/")
def start():
    return render_template("start.html")

@app.route("/lobby")
def lobby():
    return render_template("lobby.html")

@app.route("/action")
def action():
    return render_template("action.html")

@app.route("/wait")
def wait():
    return render_template("wait.html")

@app.route("/end")
def end():
    return render_template("end.html")

@app.route("/game")
def game():
    return render_template("game.html")