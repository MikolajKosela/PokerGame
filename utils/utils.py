from services.serialization import send_data, send_logs, build_start_data

def refresh_data(socketio, game):
    print("  Wyświetlam graczy, którym odświeżam dane")
    socketio.emit("startData", build_start_data(game))
    send_logs(socketio, game)
    for player in game.players:
        print(player.nickname)
        send_data(socketio, game, player.sid)

def send_error_message(socketio, content, sid):
    socketio.emit("message", {"content": content, "style": "err"}, to=sid)

def send_info_message(socketio, content, sid):
    socketio.emit("message", {"content": content, "style": "info"}, to=sid)

def send_message_to_everyone(socketio, content):
    socketio.emit("message", {"content": content, "style": None})



