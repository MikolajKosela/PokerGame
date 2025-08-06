from flask import Flask, request, render_template, url_for, redirect, session, jsonify
import random
app = Flask(__name__)
app.secret_key="tajny klucz"
global RoundNum
roundNum=0
global end
end=False
global whoseRoundIs
whoseRoundIs=-1

class Card:
    def __init__(self, color, number, visibility):
        self.color=color
        self.number=number
        self.visibility=visibility
    def isVisible(self):
        return self.visibility
    def makeVisible(self):
        self.visibility=True
    def __str__(self):
        if self.visibility:
            return f"{self.color} {self.number}"
        else:
            return f"???"
    def to_dict(self):
        return {
            "color": self.color if self.visibility else None,
            "number": self.number if self.visibility else None,
            "visible": self.visibility
        }

class Pack:
    def __init__(self):
        self.cards=[]
        colors=["Pik", "Kier", "Trefl", "Karo"]
        numbers=["4", "5", "6", "7", "8", "9", "10", "J", "K", "Q", "A"]
        for i in colors:
            for j in numbers:
                self.cards.append(Card(i, j, False))
    def shuffle_cards(self):
        random.shuffle(self.cards)
    def get_cards(self, num):
        taken_cards=[]
        for _ in range(num):
            taken_cards.append(self.cards.pop())
        return taken_cards

class Table:
    def __init__(self, pack, num):
        self.cards=pack.get_cards(num)
    def __str__(self):
        return " ".join(str(card) for card in self.cards)
    def show_card(self, num):
        for card in self.cards:
            if not card.isVisible():
                card.makeVisible()
                num-=1
            if num==0:
                break
    def to_dict(self):
        return {
            "cards": [card.to_dict() for card in self.cards]
        }

class Player:
    def __init__ (self, nickname, credits, ID):
        self.nickname=nickname
        self.ID=ID
        self.credits=credits
        self.bet=0
        self.allin=False
        self.fold=False
    def to_dict(self):
        return {
            "nickname": self.nickname,
            "credits": self.credits,
            "allin": self.allin,
            "fold": self.fold,
            "id": self.ID,
        }

class Game:
    def __init__(self):
        self.players=[]
        self.tables=[]
        self.pack=Pack()
        self.pot=0
        self.bet=1
        self.playersNum=0

    def start(self):
        self.pack.shuffle_cards()
        for _ in self.players:
            self.tables.append(Table(self.pack, 2))
        self.tables.append(Table(self.pack, 5))
        global whoseRoundIs
        whoseRoundIs=0
        if session.get("ID")==whoseRoundIs:
            return redirect(url_for("action"))
        else:
            return redirect(url_for("wait"))

    def end(self):
        global end
        end=True
        global whoseRoundIs
        whoseRoundIs=-2
        render_template("end.html")
        return redirect(url_for("end"))

    def nextRound(self):
        global whoseRoundIs
        global roundNum
        whoseRoundIs=0
        playerId=session.get("ID")

        callNeded=False
        if roundNum%2==0:
            for player in self.players:
                if player.bet<self.bet:
                    callNeded=True
                    break

        if not callNeded:
            for player in self.players:
                player.bet=0
            self.bet=0

        if not callNeded and roundNum%2==0:
            roundNum+=1
        roundNum+=1

        #0 Wchodzenie i podbijanie wejścia
        #1 Wyrównywanie wejścia
        #2 Pokazanie kart graczy i betowanie
        #3 Sprawdzanie/czekanie
        #4 Odkrycie 3 kart i betowanie
        #5 Sprawdzanie/czekanie
        #6 Odkrycie karty i betowanie
        #7 Sprawdzanie/czekanie
        #8 Odkrycie karty i betowanie
        #9 Sprawdzanie/czekanie
        #10 Podsumowanie

        if roundNum==2:
           for i in range(0, len(self.players)):
               for card in self.tables[i].cards:
                   card.makeVisible()
        elif roundNum==4:
            for i in range(0, 3):
                self.tables[-1].cards[i].makeVisible()
        elif roundNum==6 or roundNum==8:
            self.tables[-1].cards[int(roundNum/2)].makeVisible()

        if roundNum==10:
            return self.end()
        if playerId==whoseRoundIs:
            return redirect(url_for("action"))
        else:
            return redirect(url_for("wait"))

    def playerStartRound(self):
        global whoseRoundIs

    def nextPlayer(self):
        global whoseRoundIs
        whoseRoundIs+=1
        if whoseRoundIs>=len(self.players):
            return self.nextRound()
        if session.get("ID")==whoseRoundIs:
            return redirect(url_for("action"))
        else:
            return redirect(url_for("wait"))

    def check(self):
        return self.nextPlayer()
    
    def makeBet(self, amount):
        if self.players[session.get("ID")].credits>=amount and amount>0:
            self.players[session.get("ID")].credits-=amount
            self.players[session.get("ID")].bet+=amount
            self.pot+=amount
            self.bet=amount
            return self.nextPlayer()
        return redirect(url_for("action"))

    def call(self):
        cost=self.bet-self.players[session.get("ID")].bet
        print(cost)
        if self.players[session.get("ID")].credits>=cost:
            self.players[session.get("ID")].credits-=cost
            self.players[session.get("ID")].bet+=cost
            self.pot+=cost
            return self.nextPlayer()
        return redirect(url_for("action"))

    def raiseBet(self, amount):
        cost=self.bet-self.players[session.get("ID")].bet
        if self.players[session.get("ID")].credits>=amount+cost and amount>0:
            self.players[session.get("ID")].credits-=(amount+cost)
            self.players[session.get("ID")].bet+=(amount+cost)
            self.pot+=(amount+cost)
            self.bet+=amount
            return self.nextPlayer()
        return redirect(url_for("action"))

    def fold(self):
        self.players[session.get("ID")].fold=True
        self.playersNum-=1
        if self.playersNum<=1:
            for table in self.tables:
                table.show_card(len(table.cards))
            return self.end()
        return self.nextPlayer()

    def allin(self):
        self.players[session.get("ID")].allin=True
        amount=self.players[session.get("ID")].credits
        self.players[session.get("ID")].credits=0
        self.players[session.get("ID")].bet+=amount
        self.pot+=amount
        self.bet+=amount
        return self.nextPlayer()

    def again(self):
        global roundNum
        roundNum=0
        self.tables=[]
        self.bet=1
        self.pack=Pack()
        for player in self.players:
            player.bet=0
            player.allin=False
            player.fold=False
        return self.start()

game=Game()

@app.route("/", methods=["GET", "POST"])
def start():
    if request.method=="POST":
        nickname=request.form["nickname"]
        session["nickname"]=nickname
        session["ID"]=len(game.players)
        game.players.append(Player(nickname, 100, len(game.players)))
        game.playersNum=len(game.players)
        return redirect(url_for("lobby"))
    return  render_template("start.html")


@app.route("/lobby", methods=["GET", "POST"])
def lobby():
    nickname=session.get("nickname")
    if not nickname :
        return redirect(url_for("start"))
    if request.method=="POST":
        return game.start()
    return render_template("lobby.html", nickname=nickname)

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
    if whoseRoundIs==-1:
        return redirect(url_for("lobby"))
    player_id=session.get("ID")
    return render_template("wait.html")

@app.route("/whoseRound")
def whoseRound():
    if whoseRoundIs>=0:
        roundData={
                "yourId": session.get("ID"),
                "round": whoseRoundIs,
                "playerName": game.players[whoseRoundIs].nickname,
                "playerCredit": game.players[whoseRoundIs].credits,
                "pot": game.pot,
                "bet": game.bet-game.players[session.get("ID")].bet,
                "checkButton": game.players[session.get("ID")].allin or game.bet==game.players[session.get("ID")].bet,
                "betButton": not game.players[session.get("ID")].allin and roundNum%2==0 and game.bet==0,
                "callButton": not game.players[session.get("ID")].allin and game.bet>game.players[session.get("ID")].bet,
                "raiseButton": not game.players[session.get("ID")].allin and roundNum%2==0 and game.bet>0,
                "foldButton": not game.players[session.get("ID")].allin and True,
                "allinButton": roundNum%2==0 and game.players[session.get("ID")].credits>0,
                "playerBet": game.players[session.get("ID")].bet,
                "roundNum": roundNum,
                "allin": game.players[session.get("ID")].allin
        }
        return jsonify(roundData)
    else:
        roundData={
                "yourId": session.get("ID"),
                "round": whoseRoundIs,
                "pot": game.pot,
        }
        return jsonify(roundData)

@app.route("/action", methods=["POST", "GET"])
def action():
    if whoseRoundIs==-1:
        return redirect(url_for("lobby"))
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
        return redirect(url_for("wait.html"))
    return render_template("action.html", roundNum=roundNum)

@app.route("/summary")
def sumarry():
    if end==True:
        summaryData=[]
        for i, player in enumerate(game.players):
            cards=[card.to_dict() for card in game.tables[i].cards]
            summaryData.append({
                "nickname": player.nickname,
                "id": player.ID,
                "fold": player.fold,
                "credits": player.credits,
                "cards": cards,
                })
        return jsonify(summaryData)
    else:
        return jsonify({"error": "Unauthorized"}), 403

@app.route("/end", methods=["GET", "POST"])
def end():
    global end
    if request.method=="POST":
        action=request.form.get("action")
        if action=="again" and game.pot==0:
             return game.again()
        winnerId=int(action)
        if(action!="again" and winnerId>=0 and winnerId<len(game.players)):
            game.players[winnerId].credits+=game.pot
            game.pot=0
    if end==True:
        return render_template("end.html")
    return redirect(url_for("start"))

if __name__ == '__main__':
    app.run(debug = True)
