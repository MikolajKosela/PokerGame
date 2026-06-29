from flask import Flask, render_template


def register_routes(app: Flask) -> None:
    @app.route("/")
    def start() -> str:
        return render_template("start.html")

    @app.route("/lobby")
    def lobby() -> str:
        return render_template("lobby.html")

    @app.route("/action")
    def action() -> str:
        return render_template("action.html")

    @app.route("/wait")
    def wait() -> str:
        return render_template("wait.html")

    @app.route("/end")
    def end() -> str:
        return render_template("end.html")

    @app.route("/game")
    def game() -> str:
        return render_template("game.html")